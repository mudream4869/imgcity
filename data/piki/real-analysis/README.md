# 台大數學系 分析導論 部分整理

* Ext4:

$$
x \in \mathbb{A} \Rightarrow |x - \frac{p}{q}| \geq \frac{c(x)}{q^n}
$$

* Ext5: 

$$
\sum 10^{-n!} \notin \mathbb{A}    
$$

---

* $Card(2^S) > Card(S)$

---

Every open set in $\mathbb R$ is union of at most countible collection of disjoint segment.

---

$G\_\delta$ sets = countible intersect of open set
$F\_\sigma$ sets = countible union of close set

* Ext13: 

$$
Cont(f) = \\{ x \ | \ f \ cont \ @ \ x \\} = G\_\delta
$$

($\Rightarrow Cont(f) \neq \mathbb{Q}^c$ )

---

$\sum a_n$ diverge, $\sum \frac{a_n}{1 + n a_n}$ converge or diverge :

* $a_n = 1$ : diverge
* $a\_{n^2} = \frac{1}{n}$ : converge 

## Brouwer Fixed point

## Fustenberg topology

base of open set = $\\{ a + kd | k \in \mathbb Z\\}$

1. close = open
2. $|Prime| = \inf$

---

$$
S = \\{ (n\sqrt 2) \ | \ n \in \mathbb N \\} \ dense \ in \ [0, 1)
$$

pf:

1. $|S| = \inf$
2. $|S| \subset [0, 1]$

$\Rightarrow$ $\exists \ limit \ point$

$\Rightarrow$ $\forall \epsilon$ $\exists n, m \ s.t. \ |(n\sqrt 2) - (m\sqrt 2)| < \epsilon$

$\Rightarrow$ $(\\{n-m\\}\sqrt 2) < \epsilon$

o.k.

## Space-fill Curve

Let f be continous onto function. $f : [0, 1] \rightarrow [0, 1]^2$. 

Pf : $f$ not one-to-one

* let $p \in [0, 1]$, observe $[0, 1] - p$ disconnect but $[0, 1]^2 - f(p)$ connect.
* Continous map connected part to connected part.

## 2 max 0 min 0 saddle

$$ f(x, y) = -(x^2 - 1)^2 - (x^2y - x - 1)^2$$
