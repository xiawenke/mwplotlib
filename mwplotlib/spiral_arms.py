from .arms_data import ArmsData
from .utilities import utilities

import numpy as np
import astropy.units as u

class MilkyWayHandler():
    def __init__(self, plt) -> None:
        self.plt = plt
        self.arms = ArmsData()
        self.utilities = utilities()
        self.plt_colors = self._get_plt_colorcodes()
        
    def scatter(self, unit="pc"):

        if(type(unit) != str):
            unit = unit.to_string()

        # Name Alias RAh RAm      RAs DE- DEd DEm     DEs    plx   _plx    pmE  _pmE    pmN  _pmN VLSR _VLSR  Arm    Ref
        # G305.20+  G305.20+00.01   NaN  13  11  16.8912   -  62  45  55.008  0.250  0.050  -6.90  0.33  -0.52  0.33  -38     5  Nor     61
        # G339.88-  G339.88-01.25   NaN  16  52  04.6776   -  46  08  34.404  0.480  0.080  -1.60  0.52  -1.90  0.52  -34     3  Nor     37
        # G348.70-  G348.70-01.04   NaN  17  20  04.0360   -  38  58  30.920  0.296  0.026  -0.73  0.31  -2.83  0.59   -9     5  Nor      1
        # G359.61-  G359.61-00.24   NaN  17  45  39.0697   -  29  23  30.265  0.375  0.021   1.00  0.40  -1.50  0.50   21     5  Nor   1 52
        # G000.31-  G000.31-00.20   NaN  17  47  09.1092   -  28  46  16.278  0.342  0.042   0.21  0.39  -1.76  0.64   18     3  Nor     53
        # ...                 ...   ...  ..  ..      ...  ..  ..  ..     ...    ...    ...    ...   ...    ...   ...  ...   ...  ...    ...
        # G001.00-  G001.00-00.23   NaN  17  48  55.2845   -  28  11  48.240  0.090  0.057  -3.87  0.28  -6.23  0.56    2     5  ???     51
        # G002.70+  G002.70+00.04   NaN  17  51  45.9766   -  26  35  57.070  0.101  0.105  -3.13  0.87  -9.36  1.24   93     5  ???     51
        # G019.49+  G019.49+00.11   NaN  18  26  09.1691   -  11  52  51.354  0.326  0.100  -3.60  0.42  -8.20  1.03  121     5  ???      1
        # G010.47+  G010.47+00.02   NaN  18  08  38.2290   -  19  51  50.262  0.117  0.008  -3.86  0.19  -6.40  0.14   69     5  ???      7
        # G007.47+  G007.47+00.05   NaN  18  02  13.1823   -  22  27  58.981  0.049  0.006  -2.43  0.10  -4.43  0.16  -14    10  ???  62 63

        # self.arms() in pd.DataFrame format
        plotData = {"x": [], "y": [], "arm": [], "color": []}
        for thisRow in self.arms("scatter", 'dict'):
            thisRA = self.utilities.eq_RA(thisRow['RAh'], thisRow['RAm'], thisRow['RAs'])
            thisDec = self.utilities.eq_Dec(thisRow['DE-'], thisRow['DEd'], thisRow['DEm'], thisRow['DEs'])
            thisThisPX = thisRow['plx']

            thisThisDist = self.utilities.eq_parallax(thisRow['plx'], to_unit=unit)
            thisVelo = thisRow['VLSR']
            
            thisGalactic = self.utilities.to_galactic(thisRA, thisDec, thisThisDist)

            # print(thisGalactic.l.degree, thisGalactic.b.degree)

            thisProjX = thisThisDist * np.cos(thisGalactic.b.degree) * np.cos(thisGalactic.l.degree)
            thisProjY = thisThisDist * np.cos(thisGalactic.b.degree) * np.sin(thisGalactic.l.degree)
            thisArm = thisRow['Arm']

            plotData["x"].append(thisProjX)
            plotData["y"].append(thisProjY)
            plotData["arm"].append(thisArm)
        
        # plt.scatter(plotData["x"], plotData["y"], s=1, c='black')
        # plt.show()

        # Different colors for different arms
        color_codes = {}
        for thisArm in np.unique(plotData["arm"]):
            thisArmColor = self.plt_colors[np.where(np.unique(plotData["arm"]) == thisArm)[0][0]]
            color_codes[thisArm] = thisArmColor
        
        for i in range(len(plotData["arm"])):
            plotData["color"].append(color_codes[plotData["arm"][i]])
        
        # print(plotData["color"])
        self.plt.scatter(plotData["x"], plotData["y"], s=1, c=plotData["color"])
        # plt.show()
        # input()

    def shape(self, unit="kpc", style="region", step=.001, plot_type="polar", config={}, legend=True, offsets=[0, 0], rotate=0, direction="ccw", **kwargs):
        """
        config in the form of:
        {
            "Outer": {
                "color": "red", 
                "lw": 1,
                ... # Matplotlib kwargs
            }, 
            "Norma": {
                "color": "blue",
                "lw": 1,
                ... # Matplotlib kwargs
            }, 
            ...
        """
        plotData = []

        if(type(unit) != str):
            unit = unit.to_string()

        if(plot_type == "polar"):
            # set plot type to polar
            if(hasattr(self.plt, "polar")):
                self.plt.polar([], [])
            else:
                # Show warning
                print("Warning: polar plot not automatically set. If you are using ax, please add subplot_kw=dict(projection='polar') argument to your plt.subplots() call.")
                print("You may ignore this warning if the argument is already present.")

        lastArm = ""
        for thisRow in self.arms("shape", 'dict'):
            thisKwargs = {}
            if(thisRow['Spiral Arm'] in config):
                thisKwargs = config[thisRow['Spiral Arm']]
                for key in kwargs:
                    if(key not in thisKwargs):
                        thisKwargs[key] = kwargs[key]
            else: 
                thisKwargs = kwargs.copy()
            
            if(legend):
                thisKwargs["label"] = thisRow['Spiral Arm']
                    

            # print(thisRow)
            # betaRange_0 = int(thisRow['beta Range'].split('rarr')[0].strip()) / 180 * np.pi
            # betaRange_1 = int(thisRow['beta Range'].split('rarr')[1].strip()) / 180 * np.pi
            betaRange_0 = int(thisRow['beta Range'].split('rarr')[0].strip())
            betaRange_1 = int(thisRow['beta Range'].split('rarr')[1].strip())

            thisBetaRange = np.linspace(
                betaRange_0, betaRange_1, 
                int((betaRange_1 - betaRange_0) / step)
            )
            
            thisRRange = self.utilities.ed_sr_function_R(
                thisBetaRange,
                float(thisRow['R _ref'].split("+or-")[0].strip()),
                float(thisRow['beta _ref'].split("+or-")[0].strip()),
                float(thisRow['psi'].split("+or-")[0].strip())
            )
            
            thisBetaRange = thisBetaRange / 180 * np.pi
            thisArmWidth = float(thisRow['Width'].split("+or-")[0].strip())
            
            # print(thisRow['Spiral Arm'])
            # print(thisRRange)
            # print(betaRange_0, betaRange_1, float(thisRow['R _ref'].split("+or-")[0].strip()),
            #     float(thisRow['beta _ref'].split("+or-")[0].strip()),
            #     float(thisRow['psi'].split("+or-")[0].strip()))
            # print(thisBetaRange)
            # plt.plot(np.linspace(0, 1, len(thisRRange)), thisBetaRange)
            # plt.show()
            # input()

            if(unit != "kpc"):
                thisRRange_ = thisRRange * u.kpc
                thisRRange = thisRRange_.to(u.Unit(unit)).value
                thisArmWidth_ = thisArmWidth * u.kpc
                thisArmWidth = thisArmWidth_.to(u.Unit(unit)).value
            
            if(direction == "cw"):
                thisBetaRange = - thisBetaRange
            
            if(plot_type == "polar"):
                if(thisRow['Spiral Arm'] != lastArm) :
                    # self.plt.plot(thisBetaRange, thisRRange + thisArmWidth / 2, "--", label=thisRow['Spiral Arm'])
                    # self.plt.plot(thisBetaRange, thisRRange - thisArmWidth / 2, "--", label=thisRow['Spiral Arm'], color=self._get_last_color())
                    # Allow for custom kwargs:
                    if(style == "region"):
                        self.plt.plot(thisBetaRange + offsets[0] + rotate, thisRRange + offsets[1] + thisArmWidth / 2, "--", **thisKwargs)
                        self.plt.plot(thisBetaRange + offsets[0] + rotate, thisRRange + offsets[1] - thisArmWidth / 2, "--", color=self._get_last_color(), **self._kwargs_no_color(thisKwargs))
                    elif(style == "line"):
                        self.plt.plot(thisBetaRange + offsets[0] + rotate, thisRRange + offsets[1], "--", **thisKwargs)
                    else:
                        print("Invalid style")
                        return
                else:
                    # print(thisRow['Spiral Arm'])
                    if(style == "region"):
                        self.plt.plot(thisBetaRange + offsets[0] + rotate, thisRRange + offsets[1] + thisArmWidth / 2, "--", 
                            color=self._get_last_color(), **self._kwargs_no_color(thisKwargs)
                        )
                        self.plt.plot(thisBetaRange + offsets[0] + rotate, thisRRange + offsets[1] - thisArmWidth / 2, "--", 
                            color=self._get_last_color(), **self._kwargs_no_color(thisKwargs)
                        )
                    elif(style == "line"):
                        self.plt.plot(thisBetaRange + offsets[0] + rotate, thisRRange + offsets[1], "--", 
                            color=self._get_last_color(), **self._kwargs_no_color(thisKwargs)
                        )
                    else:
                        print("Invalid style")
                        return

                # self.plt.show()
                # input()
            elif(plot_type == "cartesian"):
                thisX = thisRRange * np.cos(thisBetaRange + rotate)
                thisY = thisRRange * np.sin(thisBetaRange + rotate)
                thisX_regionUpper = (thisRRange + thisArmWidth / 2) * np.cos(thisBetaRange + rotate)
                thisY_regionUpper = (thisRRange + thisArmWidth / 2) * np.sin(thisBetaRange + rotate)
                thisX_regionLower = (thisRRange - thisArmWidth / 2) * np.cos(thisBetaRange + rotate)
                thisY_regionLower = (thisRRange - thisArmWidth / 2) * np.sin(thisBetaRange + rotate)
                if(thisRow['Spiral Arm'] != lastArm) :
                    # self.plt.plot(thisBetaRange, thisRRange + thisArmWidth / 2, "--", label=thisRow['Spiral Arm'])
                    # self.plt.plot(thisBetaRange, thisRRange - thisArmWidth / 2, "--", label=thisRow['Spiral Arm'], color=self._get_last_color())
                    # Allow for custom kwargs:
                    if(style == "region"):
                        self.plt.plot(thisX_regionUpper + offsets[0], thisY_regionUpper + offsets[1], "--", **thisKwargs)
                        self.plt.plot(thisX_regionLower + offsets[0], thisY_regionLower + offsets[1], "--", color=self._get_last_color(), **self._kwargs_no_color(thisKwargs))
                    elif(style == "line"):
                        self.plt.plot(thisX + offsets[0], thisY + offsets[1], "--", **thisKwargs)
                    else:
                        print("Invalid style")
                        return
                else:
                    # print(thisRow['Spiral Arm'])
                    if(style == "region"):
                        self.plt.plot(thisX_regionUpper + offsets[0], thisY_regionUpper + offsets[1], "--", 
                            color=self._get_last_color(), **self._kwargs_no_color(thisKwargs)
                        )
                        self.plt.plot(thisX_regionLower + offsets[0], thisY_regionLower + offsets[1], "--", 
                            color=self._get_last_color(), **self._kwargs_no_color(thisKwargs)
                        )
                    elif(style == "line"):
                        self.plt.plot(thisX + offsets[0], thisY + offsets[1], "--", 
                            color=self._get_last_color(), **self._kwargs_no_color(thisKwargs)
                        )
                    else:
                        print("Invalid style")
                        return
            else:
                print("Invalid plot type")
                return    

            lastArm = thisRow['Spiral Arm']
                    
            # plt.show()
            # input()
        # self.plt.legend()
        # self.plt.show()
        
    def _get_last_color(self):
        # return self.plt.gca().lines[-1].get_color()
        # It is possible that the user is using ax instead of plt
        if(hasattr(self.plt, "gca")):
            return self.plt.gca().lines[-1].get_color()
        elif(hasattr(self.plt, "get_lines")):
            return self.plt.get_lines()[-1].get_color()
        else:
            print("Invalid plt object")
            return None
    
    def _get_plt_colorcodes(self):
        # return self.plt.rcParams['axes.prop_cycle'].by_key()['color']
        # It is possible that the user is using ax instead of plt
        if(hasattr(self.plt, "rcParams")):
            return self.plt.rcParams['axes.prop_cycle'].by_key()['color']
        else:
            import matplotlib.pyplot as plt
            return plt.rcParams['axes.prop_cycle'].by_key()['color']

    def _kwargs_no_color(self, kwargs):
        # Remove color from kwargs
        if('color' in kwargs):
            kwargs.pop('color')
        
        # remove label from kwargs
        if('label' in kwargs):
            kwargs.pop('label')

        return kwargs
            
class MilkyWay():
    def mw_plt(plt):
        plt.MilkyWay = MilkyWayHandler(plt)
        return plt
