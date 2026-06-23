import pandas as pd
import numpy as np
from pulp import *
import matplotlib.pyplot as plt


class Gas_Turbine_Asset:

    def __init__(self, capacity_mw, fuel_cost_eur, max_hours, engine):
        self.capacity_mw = capacity_mw
        self.fuel_cost_eur = fuel_cost_eur
        self.max_hours = max_hours
        self.engine = engine
    
    def load_prices(self, filepath: str):
        df = pd.read_excel(filepath)
        return df
    
    def solver(self, df, output):
        
        # --- Defining the problem --- #
        problem = LpProblem("Gas Dispatcher", LpMaximize)

        # --- Variable to solve, dispatch or not dispatch? --- #
        Dispatch = {
            i : LpVariable(f"Dispatch{i}", cat="Binary")
            for i in df.index
        }
        
        # --- Problem to Solve --- #
        Profit = lpSum(((df.loc[i,"price_eur_mwh"]-self.fuel_cost_eur)*self.capacity_mw*Dispatch[i]*0.25)
                       for i in df.index
        )
        problem += Profit

        # --- Constraints --- #
        problem += lpSum((Dispatch[i])
                        for i in df.index
        ) <= self.max_hours*4

        problem.solve()

        self.results = pd.DataFrame({
            "Time" : df["datetime"],
            "Electricity Prices" : df["price_eur_mwh"],
            "Dispatch" : [int(value(Dispatch[i])) for i in df.index],
            "Profit": [int(value(Dispatch[i])) * (df.loc[i, "price_eur_mwh"] - self.fuel_cost_eur) * self.capacity_mw * 0.25 for i in df.index],
        })

        self.results.to_excel(output)
    
    def plot_dispatch(self):
        fig, ax1 = plt.subplots(figsize=(12,8))

        # Plot first line on left y-axis
        line1 = ax1.plot(self.results["Time"], self.results["Dispatch"], color='grey', label='Dispatch')
        ax1.set_xlabel("Datetime")
        ax1.set_ylabel('Dispatch')

        # Create second y-axis sharing same x-axis
        ax2 = ax1.twinx()

        # Plot second line on right y-axis
        line2 = ax2.plot(self.results["Time"], self.results["Profit"], color='lightblue', label="Profit")
        ax2.set_ylabel('Profit')

        plt.tight_layout()
        plt.show()
    
if __name__ == "__main__":
    gt = Gas_Turbine_Asset(10, 38, 16, "Siemens")
    df = gt.load_prices(r"C:\Users\ola06\Downloads\gas_turbine_prices.xlsx")
    prof = gt.solver(df, r"C:\Users\ola06\OneDrive\Desktop\Summit_Python\Python\Excercism\Preparation_Phase3\dispatcher.xlsx")
    display = gt.plot_dispatch()
    print(df.info())