import time
from typing import List

from .types import LLMTask
from .metrics import base_metric
from ..api_objects.dataset import dataset
from ..api_objects.experiment import experiment_item
from ..api_objects import opik_client

from . import tasks_scorer, scores_logger, report, evaluation_result


def evaluate(
    dataset: dataset.Dataset,
    task: LLMTask,
    scoring_metrics: List[base_metric.BaseMetric],
    experiment_name: str,
    verbose: int = 1,
    task_threads: int = 16,
) -> evaluation_result.EvaluationResult:
    """
    Performs task evaluation on a given dataset.

    Args:
        dataset: An Opik dataset instance

        task: A callable object that takes DatasetItem as input and returns
            dictionary which will later be used for scoring

        scoring_metrics: List of metrics to calculate during evaluation.
            Each metric has `score(...)` method, arguments for this method
            are taken from the `task` output, check the signature
            of the `score` method in metrics that you need to find out which keys
            are mandatory in `task`-returned dictionary.

        task_threads: amount of thread workers to run tasks. If set to 1, no additional
            threads are created, all tasks executed in the current thread sequentially.
            are executed sequentially in the current thread.
            Use more than 1 worker if your task object is compatible with sharing across threads.
    """
    client = opik_client.get_client_cached()
    start_time = time.time()

    test_results = tasks_scorer.run(
        client=client,
        dataset_=dataset,
        task=task,
        scoring_metrics=scoring_metrics,
        workers=task_threads,
        verbose=verbose,
    )

    total_time = time.time() - start_time

    if verbose == 1:
        report.display_experiment_results(dataset.name, total_time, test_results)

    scores_logger.log_scores(client=client, test_results=test_results)

    experiment = client.create_experiment(
        name=experiment_name, dataset_name=dataset.name
    )
    experiment_items = [
        experiment_item.ExperimentItem(
            dataset_item_id=result.test_case.dataset_item_id,
            trace_id=result.test_case.trace_id,
        )
        for result in test_results
    ]

    experiment.insert(experiment_items=experiment_items)

    client.flush()

    evaluation_result_ = evaluation_result.EvaluationResult(
        experiment_id=experiment.id,
        experiment_name=experiment.name,
        test_results=test_results,
    )
    return evaluation_result_
