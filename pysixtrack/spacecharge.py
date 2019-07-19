from scipy.constants import e as qe
from scipy.constants import c as clight

from pysixtrack.base_classes import Element
from .gaussian_fields import get_Ex_Ey_Gx_Gy_gauss


class SpaceChargeCoast(Element):
    """Space charge for a coasting beam"""

    _description = [
        ('line_density', '1/m', "Desc...", 0.), 
        ('sigma_x', 'm', "Desc...", 1.),
        ('sigma_y', 'm', "Desc...", 1.),
        ('length', 'm', "Desc...",0.),
        ('Delta_x', 'm', "Desc...", 0.),
        ('Delta_y', 'm', "Desc...", 0),
        ]
    _extra = [
        ('min_sigma_diff', 'm', "Desc...", 1e-30),
        ('enabled', '', "Desc...", True),
        ]

    def track(self, p):
        if self.enabled:
            length = self.length
            sigma_x = self.sigma_x
            sigma_y = self.sigma_y

            charge = p.qratio*p.q0*qe
            x = p.x - self.Delta_x
            px = p.px
            y = p.y - self.Delta_y
            py = p.py

            chi = p.chi

            beta = p.beta0/p.rvv
            p0c = p.p0c*qe

            Ex, Ey = get_Ex_Ey_Gx_Gy_gauss(x, y, sigma_x, sigma_y,
                                           min_sigma_diff=1e-10, skip_Gs=True, mathlib=p._m)

            fact_kick = chi * self.line_density * charge * charge * \
                (1-beta*beta)/p0c * self.length

            px += (fact_kick*Ex)
            py += (fact_kick*Ey)

            p.px = px
            p.py = py


class SpaceChargeBunched(Element):
     _description = [
        ('number_of_particles', '', "Desc...", 0.), 
        ('bunchlength_rms', 'm', "Desc...", 1.), 
        ('sigma_x', 'm', "Desc...", 1.),
        ('sigma_y', 'm', "Desc...", 1.),
        ('length', 'm', "Desc...",0.),
        ('Delta_x', 'm', "Desc...", 0.),
        ('Delta_y', 'm', "Desc...", 0),
        ]
    _extra = [
        ('min_sigma_diff', 'm', "Desc...", 1e-30),
        ('enabled', '', "Desc...", True),
        ]

    def track(self, p):
        if self.enabled:
            pi = p._m.pi
            exp = p._m.exp
            sqrt = p._m.sqrt
            bunchlength_rms = self.bunchlength_rms
            length = self.length
            sigma_x = self.sigma_x
            sigma_y = self.sigma_y

            charge = p.qratio*p.q0*qe
            x = p.x - self.Delta_x
            px = p.px
            y = p.y - self.Delta_y
            py = p.py
            sigma = p.sigma

            chi = p.chi

            beta = p.beta0/p.rvv
            p0c = p.p0c*qe

            Ex, Ey = get_Ex_Ey_Gx_Gy_gauss(x, y, sigma_x, sigma_y,
                                           min_sigma_diff=1e-10, skip_Gs=True, mathlib=p._m)

            fact_kick = chi * charge * charge * (1-beta*beta)/p0c * length

            fact_kick *= self.number_of_particles / (bunchlength_rms*sqrt(2*pi)) * \
                                    exp(-0.5*(sigma/bunchlength_rms)*(sigma/bunchlength_rms))

            px += (fact_kick*Ex)
            py += (fact_kick*Ey)

            p.px = px
            p.py = py