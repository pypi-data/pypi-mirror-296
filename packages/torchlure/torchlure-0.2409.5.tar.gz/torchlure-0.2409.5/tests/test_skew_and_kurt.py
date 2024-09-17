import pytest
import scipy.stats
import torch

import torchlure as lure


def test_kurtosis_normal_distribution():
    data_normal = torch.randn(100000)
    kurt_normal = lure.kurtosis(data_normal, unbiased=True, fisher=True)
    kurt_normal_scipy = scipy.stats.kurtosis(data_normal.numpy(), fisher=True, bias=False)

    assert abs(kurt_normal.item() - kurt_normal_scipy) < 0.1


def test_skew_normal_distribution():
    data_normal = torch.randn(100000)
    skew_normal = lure.skew(data_normal, unbiased=True)
    skew_normal_scipy = scipy.stats.skew(data_normal.numpy(), bias=False)

    assert abs(skew_normal.item() - skew_normal_scipy) < 0.1


def test_kurtosis_uniform_distribution():
    data_uniform = torch.rand(100000)
    kurt_uniform = lure.kurtosis(data_uniform, unbiased=True, fisher=True)
    kurt_uniform_scipy = scipy.stats.kurtosis(data_uniform.numpy(), fisher=True, bias=False)

    assert abs(kurt_uniform.item() - kurt_uniform_scipy) < 0.1


def test_skew_uniform_distribution():
    data_uniform = torch.rand(100000)
    skew_uniform = lure.skew(data_uniform, unbiased=True)
    skew_uniform_scipy = scipy.stats.skew(data_uniform.numpy(), bias=False)

    assert abs(skew_uniform.item() - skew_uniform_scipy) < 0.1
