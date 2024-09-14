import os
import time
from functools import wraps

from bio_compose.processing_tools import get_job_signature
from bio_compose.runner import SimulationRunner, SimulationResult
from bio_compose.verifier import Verifier, VerificationResult


__all__ = [
    'get_compatible_verification_simulators',
    'verify'
]

API_VERIFIER = Verifier()
API_RUNNER = SimulationRunner()


def get_compatible_verification_simulators(entrypoint_file: str, return_versions: bool = False) -> list:
    return API_VERIFIER.get_compatible(entrypoint_file, return_versions)


def verify(*args) -> VerificationResult:
    """Verify and compare the outputs of simulators for a given entrypoint file of either sbml or omex.

    :param args: Positional arguments

    * 1 argument: submit omex verification with no time params. **OMEX verification only**.
    * 2 arguments: omex filepath, simulators to include in the verification. **OMEX verification only**.
    * 4 arguments: sbml filepath, start, stop, steps. **SBML verification only**.
    * 5 arguments: sbml filepath, start, stop, steps, simulators. **SBML verification only**.

    :return: instance of verification results.
    :rtype: bio_compose.verifier.VerificationResult
    """
    verifier = API_VERIFIER

    if len(args) == 0:
        raise ValueError('At least one positional argument defining a file entrypoint is required.')

    if len(args) == 2:
        simulators = args[1]
    elif len(args) == 5:
        simulators = args[4]
    else:
        simulators = ['amici', 'copasi', 'tellurium']

    run_sbml = False
    for arg in args:
        if isinstance(arg, int):
            run_sbml = True
    submission = None

    # parse executor and run
    timeout = 50
    buffer_time = 5
    poll_time = 5
    submission_generator = verifier.verify_sbml if run_sbml else verifier.verify_omex
    print("Submitting verification...")
    time.sleep(buffer_time)

    # fetch params
    submission = submission_generator(*args)
    job_id = submission.get('job_id')

    # poll gateway for results
    n_attempts = 0
    output = {}
    if job_id is not None:
        # polling loop
        while True:
            # quit after reaching timeout
            n_attempts += 1
            if n_attempts == timeout:
                print('Timeout reached. Please try to call the function again.')
                break

            # get result after buffering (submission) or refresh if re-iteration
            verification_result = verifier.get_output(job_id=job_id)

            # report job status
            current_status = verifier.get_output(job_id=job_id).get('content', {}).get('status', '')
            print(f'> Status for job ending in {get_job_signature(job_id)}: {current_status} ')

            # finish if job failed or completed, otherwise re-poll
            stop_conditions = ["COMPLETED", "FAILED"]
            job_finished = any([current_status.endswith(condition) for condition in stop_conditions])
            if not job_finished:
                time.sleep(poll_time)
            else:
                output = verifier.get_output(job_id=job_id)
                break

    return VerificationResult(data=output)


def run_simulation(*args, **kwargs) -> SimulationResult:
    """Run a simulation with BioCompose.

    :param args: Positional arguments
    * 1 argument: smoldyn simulation configuration in which time parameters (dt, duration) are already defined. **Smoldyn simulation only**.
    * 3 arguments: smoldyn configuration file, smoldyn simulation duration, smoldyn simulation dt. **Smoldyn simulation only**.
    * 5 arguments: sbml filepath, simulation start, simulation end, simulation steps, simulator. **SBML simulation only**.

    :param kwargs: Keyword arguments

    :return: instance of simulation results.
    :rtype: bio_compose.runner.SimulationResult
    """
    # set up submission
    runner = SimulationRunner()
    in_file = args[0]
    n_args = len(args)
    submission = None
    if n_args == 1:
        submission = runner.run_smoldyn_simulation(smoldyn_configuration_filepath=in_file)
    elif n_args == 3:
        dur = args[1]
        dt = args[2]
        submission = runner.run_smoldyn_simulation(smoldyn_configuration_filepath=in_file, duration=dur, dt=dt)
    elif n_args == 5:
        start = args[1]
        end = args[2]
        steps = args[3]
        simulator = args[4]
        submission = runner.run_utc_simulation(sbml_filepath=in_file, start=start, end=end, steps=steps, simulator=simulator)
    # fetch result params
    job_id = submission.get('job_id')
    output = {}
    timeout = kwargs.get('timeout', 100)
    # poll gateway for results
    i = 0
    if job_id is not None:
        print(f'Submission Results for Job ID {job_id}: ')
        while True:
            if i == timeout:
                break
            simulation_result = runner.get_output(job_id=job_id)
            if isinstance(simulation_result, dict):
                status = simulation_result['content']['status']
                last4 = get_job_signature(job_id)
                if not 'COMPLETED' in status:
                    print(f'Status for job ending in {last4}: {status}')
                    i += 1
                    time.sleep(1)
                else:
                    output = simulation_result
                    break
            else:
                i += 1
    return SimulationResult(data=output)