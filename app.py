from flask import Flask, render_template, request
import numpy as np
import math

app = Flask(__name__)

def conversion(t, Ca_0, Cb_0, k,R):
    
    if Cb_0 > Ca_0 :
        lam = Ca_0 / Cb_0
        rho = -k * (Cb_0 - Ca_0) * (math.pi * (R**2))
        Xa = (1-math.exp(rho * t) ) / (lam  - 1* math.exp(rho * t))
    
    elif Ca_0 > Cb_0:
        lam = Cb_0 / Ca_0
        rho = -k * (Ca_0 - Cb_0) * (math.pi * (R**2))
        Xb = (1-math.exp(rho * t) ) / (lam  - 1* math.exp(rho * t))
        Xa = Xb / lam
        
    else :
        V = math.pi * R *R *t 
        Xa = 1- (1/(1-k*Ca_0*Ca_0*V))
        
        
    return Xa

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get form data
        Ca_0 = float(request.form["Ca_0"])
        Fa_0 = float(request.form["Fa_0"])
        Cb_0 = float(request.form["Cb_0"])
        T_0 = float(request.form["T_0"])
        T_c = float(request.form["T_c"])
        R = float(request.form["R"])
        
        L = 1.00  # length of PFR
        H_rxn = 100  # heat of reaction in kJ
        k = 1.00  # rate constant

        A = math.pi * (R ** 2)
        Vol_flowrate = Fa_0 / Ca_0
        u = Vol_flowrate / A
        t = L / u
        Xa_e = conversion(t, Ca_0, Cb_0, k,R)
 
        max_heat_of_rxn = H_rxn * Fa_0 * Xa_e
        U = max_heat_of_rxn / (A * (T_0 - T_c))

        return render_template("index.html", heat_of_rxn=max_heat_of_rxn, htc=U)

    return render_template("index.html")


if __name__ == "__main__":
    app.run()