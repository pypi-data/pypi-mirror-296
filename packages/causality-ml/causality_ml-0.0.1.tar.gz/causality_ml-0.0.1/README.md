# Causality

Welcome to the causality library!  Yet another causality library for doing causal inference.  This library is nothing special and doesn't intend to be.  It's really just for me, so I can build the interfaces I want.  Use it if you want to, it has an MIT license.  Don't if you don't want to!

There are lots of great causality frameworks out there:
* causalml
* causaldiscovery
* causalens
* do-why
* bn-learn 

Also please checkout [this](https://github.com/matteocourthoud/awesome-causal-inference/blob/main/src/libraries.md) repo which has a bunch more!

## How To Install

`python -m pip install causality`

## Erreta

Currently this library is in alpha release.  It's mostly just design and a few ideas at this point.  Please don't take anything in here too seriously.  I plan to flesh this thing out over time.  Right now it's more or less a wrapper with some reference implementations.  But the plan is to really turn this into something special.

I think either I want this to be written in mostly C & Cython.  Or maybe jax?  Which I think could be super super cool.  Ideally there are interfaces for getting p-values and confidence intervals for every single thing that does statistics.  Don't ask me how that will work yet.  Also, I'd like to include bayesian credible intervals and bayes factor.  I think it'd also be great to include permutation and boot straps where possible.  Just really be able to analyze everything from every direction.  Maybe even some SHAP, LIME and other related interpretability measures within the ML space.  Some custom measures on neural networks might be cool too.  Or something that includes the information theoretic ideas from the bottleneck principal paper.

Of course, I'll include ATE, CATE, ATT and few other causal inference conventions.  