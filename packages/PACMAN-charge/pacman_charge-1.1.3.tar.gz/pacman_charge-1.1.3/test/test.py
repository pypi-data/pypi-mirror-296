from PACMANCharge import pmcharge
pmcharge.predict(cif_file="./Cu-BTC.cif",charge_type="REPEAT",digits=10,atom_type=True,neutral=True)
pmcharge.Energy(cif_file="./Cu-BTC.cif")