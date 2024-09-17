import pickle

with open('/home/jnovo/Desktop/InterpolationTest/Library/lib/pickle/interpolator_f.pkl', 'rb') as f:
	IntAF  = pickle.load(f)

def newsol(newa: float, newb: float) -> float:
	return IntAF(newa, newb)