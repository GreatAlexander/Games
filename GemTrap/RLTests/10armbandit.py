# -*- coding: utf-8 -*-

#==============================================================================
#  10 Arm Bandit Testbed - by Alejandro Bordallo
# Details: 
# TODO:
#==============================================================================

#==============================================================================
import os, sys, time
import numpy as np
import matplotlib.pyplot as plt

def main():
	
	n = 10
	T = 2000
	ConstA = 0.1
#	Q = np.random.randint(maxrew, size=n)
	Q = np.random.normal(size=n)
	runs = 5
	print Q
	
	probs = np.zeros(n)
	
	for run in range(runs):
		
		# Parameter selector
		if run == 0:
			e = 0
		elif run == 1:
			e = 0.01
		elif run == 2:
			e = 0.1
		elif run == 3:
			temp = 0.5
		elif run == 4:
			temp = 5
		else:
			continue


		Qest = np.zeros(n)
#		Qest = np.ones(n) * 5	# Optimistic Start
		samples = np.zeros(n)
		expsum = np.zeros(n)
		cumreward = 0
		reward = np.zeros(T)
		avgreward = np.zeros(T)
		
		for t in range(T):
			
			ran = np.random.randint(100)
			
			if run >= 3:
				
				denom = 0
				for i in range(n):
					denom = denom + np.exp(Qest[i] / temp)
				
				for a in range(n):
					probs[a] = np.exp(Qest[a]/temp) / denom
				
				probsum = 0
				a = -1
				
				for i in range(n):
					if a != -1:
						continue
					
					if ran < (probs[i] + probsum) * 100:
						a = i
					else:
						probsum = probsum + probs[i]
					
					
			else:
				
				if ran < e * 100:
					# Explore
					ranind = np.random.randint(n)
					a = ranind
				
				else:
					# Exploit
					astar = np.argmax(Qest)
					a = astar
				
#			Qsample = np.random.normal(Q[a], 0.1)
			Qsample = Q[a]
			
			expsum[a] = expsum[a] + Qsample
			
			# Weighted Average
			Qest[a] = Qest[a] + (1 / (samples[a]+1)) * (Qsample - Qest[a])
			
			# Constant Step Size
#			Qest[a] = Qest[a] + ConstA * (Qsample - Qest[a])
			
			samples[a] = samples[a] + 1
			
#			Qest[a] = expsum[a] / samples[a]
			
			if 0 < t <= 2000:
				cumreward = cumreward + Qsample
				reward[t] = Qsample
				avgreward[t] = cumreward / t
			
		
#		print avgreward
#		print Qest
#		print samples
#		print expsum
		
		xaxis = np.arange(0,T,1)
#		print xaxis
#		print avgreward
		
#		plt.plot(xaxis,reward)
		plt.plot(xaxis,avgreward)
		plt.ylabel('Average Reward')
		plt.xlabel('Plays')
		plt.show()
		plt.ylim([0,np.amax(Q) + np.amax(Q) / 2])
		plt.xlim([-10,1500])
		
		print Qest
		
		
	
	print probs		
	
	plt.plot([0, T],[np.amax(Q), np.amax(Q)], 'k--')

#==============================================================================
	#  Run if called

if __name__ == '__main__':
	main()

#==============================================================================