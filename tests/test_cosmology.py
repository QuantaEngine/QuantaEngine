from quantaengine import UniverseParams
from quantaengine.cosmology import FriedmannBackground


def test_background_expands_for_positive_density():
    params = UniverseParams(initial_scale_factor=0.01, time_step=0.001)
    bg = FriedmannBackground(params)
    a0 = bg.state.scale_factor
    bg.step(params.time_step)
    assert bg.state.scale_factor > a0
    assert bg.hubble() >= 0
