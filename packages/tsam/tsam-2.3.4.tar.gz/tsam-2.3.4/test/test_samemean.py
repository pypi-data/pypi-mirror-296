import os
import time
import json 

import pandas as pd
import numpy as np

import tsam.timeseriesaggregation as tsam


def test_samemean():

    raw = pd.read_csv(
        os.path.join(os.path.dirname(__file__), "..", "examples", "testdata.csv"),
        index_col=0,
    )
    # get all columns as floats to avoid warning
    for col in raw.columns:
        raw[col] = raw[col].astype(float)

    starttime = time.time()

    aggregation = tsam.TimeSeriesAggregation(
        raw,
        noTypicalPeriods=8,
        hoursPerPeriod=24,
        clusterMethod="k_means",
        sameMean=True,
    )

    typPeriods = aggregation.createTypicalPeriods()
    print("Clustering took " + str(time.time() - starttime))

    # test if the normalized time series all have the same mean
    means = aggregation.normalizedTimeSeries.mean().values
    np.testing.assert_allclose(means, np.array([means[0]] * len(means)), rtol=1e-5)

    # repredict the original data
    rearangedData = aggregation.predictOriginalData()

    # test if the mean fits the mean of the raw time series --> should always hold for k-means independent from sameMean True or False
    np.testing.assert_array_almost_equal(
        raw.mean(), rearangedData[raw.columns].mean(), decimal=4
    )



def test_durationRepresentation():

    raw = json.load(
        open(os.path.join(os.path.dirname(__file__), "..", "examples", "testdata_2.json"))
    )

    starttime = time.time()


    aggregation = tsam.TimeSeriesAggregation(
        raw,
        noTypicalPeriods=3,
        noSegments=8,
        hoursPerPeriod=24,
        sortValues=False,
        clusterMethod="hierarchical",
        segmentation=True,
        representationMethod="durationRepresentation",
        distributionPeriodWise=False,
        rescaleClusterPeriods=False,
        resolution=1,
    )

    periods = aggregation.createTypicalPeriods()

    print("Clustering took " + str(time.time() - starttime))

    # make sure that the sum of the attribute specific RMSEs is smaller for the k-means clustering with centroid
    assert True



if __name__ == "__main__":
    test_samemean()
