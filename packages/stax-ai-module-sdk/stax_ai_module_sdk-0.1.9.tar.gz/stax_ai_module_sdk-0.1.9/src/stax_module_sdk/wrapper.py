# See LICENSE.md file in project root directory

import os
import json
import shutil
import signal
import traceback
from datetime import datetime
from retry_requests import retry, RSession

from .Stax import Stax

sess = retry(RSession(timeout=30), retries=3)

def log(*args):
    print("[" + str(datetime.now()) + "]", *args)

def result(obj):
    with open('response.json', 'w') as f:
        json.dump(obj, f)

# Define module wrapper decorator
def def_module(module_id:str, module_key:str):
    def wrapper(app):
        def inner(*args, **kwargs):
            TEST = "test" in kwargs and kwargs["test"]

            # Setup keyboard interrupt handler (if worker is killed)
            signal.signal(signal.SIGINT, signal.default_int_handler)

            # Load request.json file
            if not os.path.exists('request.json'):
                raise Exception("Missing request.json file.")

            with open('request.json') as f:
                req = json.load(f)

            try:
                job:str = req["jobId"]
                team:str = req["teamId"]
                document:str = req["documentId"]
                stack:str = req["stackId"]
                step:str = req["stepId"]
                stepN:str = req["step"]
                config:list[dict] = req["config"]

            except:
                raise Exception("Missing required fields in request.json.")

            # Step identifier to report status to the Stax.ai API
            report = {
                "step": stepN,
                "stepId": step,
                "stack": stack,
            }

            # Instantiate a Stax.ai API object
            stax = Stax(
                module_id=module_id,
                module_key=module_key,
                team_id=team,
                document=document,
                api_url=os.getenv('STAX_API_URL', default='https://api.stax.ai')
            )

            try:
                # before we even try to do anything else, let's try to set the startTime value in the job object in the DB.
                # we will send a stax api request over to the job/start endpoint. If the job already is running or
                # completed already then it will return a 429 error, if not it will be 200 and we can continue on 
                # with the code. 
                if not TEST:
                    try:
                        # note that job_start_res isn't used anywhere but we'll keep it here for debugging purposes.
                        stax.post('/job/start/', {"jobId": job})
    
                    except Exception as e:
                        if '429' in str(e):
                            log("Job not found or job is running / completed for job ID:", job)
                            exit()

                log("Started job:", job)
                
                # Call module/app function
                count = app(stax, document, stack, team, config)

                # Finished job, post result to Stax.ai API
                result({ "status": "Complete", "units": count })
                if not TEST:
                    stax.post('/job/complete/' + job, {
                        **report,
                        "count": count
                    })

                log("Completed job:", job)

            except KeyboardInterrupt:
                log("SIGINT Received. Stopping job:", job)
                result({ "status": "Killed" })

                # Let the Stax.ai API know what happened so it can handle it
                if not TEST:
                    stax.post('/job/complete/' + job, {
                        **report,
                        "error": "Automate module worker was stopped. This job should be retried shortly."
                    })

                exit()

            except Exception as e:
                log("Error in job:", job)
                trace = traceback.format_exc()
                print(trace)

                error = {
                    "error": str(e),
                    "traceback": str(trace)
                }
                result({ "status": "Error", **error })

                # Report error to the Stax.ai API
                if not TEST:
                    stax.post('/job/complete/' + job, {
                        **report,
                        **error
                    })

            finally:
                # Delete tmp working directory
                if os.path.exists('./tmp'):
                    shutil.rmtree('./tmp')

        return inner
    return wrapper