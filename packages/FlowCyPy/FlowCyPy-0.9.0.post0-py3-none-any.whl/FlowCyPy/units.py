# Initialize a unit registry
import pint_pandas as pint

ureg = pint.PintType.ureg

ureg.setup_matplotlib()
Quantity = ureg.Quantity

power = ureg.watt.dimensionality
watt = ureg.watt
milliwatt = ureg.milliwatt
microwatt = ureg.microwatt

volt = ureg.volt
millivolt = ureg.millivolt
microvolt = ureg.microvolt

particle = ureg.particle

refractive_index_unit = ureg.refractive_index_unit
degree = ureg.degree

distance = ureg.meter.dimensionality
meter = ureg.meter
millimeter = ureg.millimeter
micrometer = ureg.micrometer
nanometer = ureg.nanometer

time = ureg.second.dimensionality
second = ureg.second
millisecond = ureg.millisecond
microsecond = ureg.microsecond

volume = ureg.liter.dimensionality
liter = ureg.liter
milliliter = ureg.milliliter
microliter = ureg.microliter

frequency = ureg.hertz.dimensionality
hertz = ureg.hertz
kilohertz = ureg.kilohertz
megahertz = ureg.megahertz
gigahertz = ureg.gigahertz