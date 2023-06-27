import astropy.units as u
import astropy.constants as c
import astropy.coordinates as coord
import numpy as np

class utilities():
    def eq_parallax(self, px, from_unit="mas", to_unit="pc"):
        """
        Convert parallax to distance.
        """
        
        return (
            (1 / (px * u.Unit(from_unit)).to(u.mas)) * u.pc
        ).to(u.Unit(to_unit)).value
    
    def eq_RA(self, RA1, RA2, RA3):
        """
        Convert RA to degrees.
        """

        # print(RA1, RA2, RA3)

        return coord.Angle(
            "{}h{}m{}s".format(RA1, RA2, RA3)
        ).degree

    def eq_Dec(self, Dec_sign, Dec1, Dec2, Dec3):
        """
        Convert Dec to degrees.
        """

        return coord.Angle(
            "{}{}d{}m{}s".format(Dec_sign, Dec1, Dec2, Dec3)
        ).degree

    def ed_sr_function_R(self, beta, R_ref, beta_ref, psi):
        """
        Spiral-arm-fitting Function
        ref: DOI 10.3847/1538-4357/acc45c (Eq. 2)
        """
        beta = beta / 180 * np.pi
        beta_ref = beta_ref / 180 * np.pi
        return R_ref * np.exp(
            - (beta - beta_ref) * np.tan(psi / 180 * np.pi)
        )

    def to_galactic(self, RA, Dec, Dist):
        """
        Convert RA and Dec to Galactic coordinates.
        """
    
        return coord.SkyCoord(
            ra=RA * u.degree,
            dec=Dec * u.degree,
            distance=Dist * u.pc,
            frame='icrs'
        ).galactic
