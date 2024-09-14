# Generate galaxy samples via integrating SDE with ScoreNet gradients

from .scorenet import HSC_32, HSC_64, ZTF_32, ZTF_64, QUASAR_72
import jax
import functools as ft
import diffrax as dfx
import jax.numpy as jnp
import jax.random as jr
import equinox as eqx


int_beta = lambda t: t
weight = lambda t: 1 - jnp.exp(-int_beta(t))


@eqx.filter_jit
def single_sample_fn(model, int_beta, data_shape, dt0, t1, key):
    def drift(t, y, args):
        _, beta = jax.jvp(int_beta, (t,), (jnp.ones_like(t),))
        return -0.5 * beta * (y + model(y, t))

    term = dfx.ODETerm(drift)
    solver = dfx.Tsit5()
    t0 = 0.0
    y1 = jr.normal(key, data_shape)
    # reverse time, solve from t1 to t0
    sol = dfx.diffeqsolve(term, solver, t1, t0, -dt0, y1)
    return sol.ys[0]


def generateSamples(n_samples=1, hi_res=True, seed=1992):
    if hi_res:
        model = HSC_ScoreNet64
        data_shape = (1, 64, 64)
    else:
        model = HSC_ScoreNet32
        data_shape = (1, 32, 32)

    # create samples
    key = jr.PRNGKey(seed)
    sample_size = n_samples
    dt0 = 0.025  # sample step size
    sample_key = jr.split(key, sample_size)
    sample_fn = ft.partial(single_sample_fn, model, int_beta, data_shape, dt0, t1=10.0)
    sample = jax.vmap(sample_fn)(sample_key)

    return sample
