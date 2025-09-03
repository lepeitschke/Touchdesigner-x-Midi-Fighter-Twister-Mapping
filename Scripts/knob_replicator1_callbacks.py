# me - this DAT
# 
# comp - the replicator component which is cooking
# allOps - a list of all replicants, created or existing
# newOps - the subset that were just created
# template - table DAT specifying the replicator attributes
# master - the master operator
#

def onRemoveReplicant(comp, replicant):

	replicant.destroy()
	return

def onReplicate(comp, allOps, newOps, template, master):

	for c in newOps:
		#c.display = True
		#c.render = True
		c.par.display = 1
		
		# reset LED status to make it susceptable to new values
		midiout = c.op("constant1")
		midiout.par.value0 = 0
		# Run the existing chopexec2 DAT inside the replicants to initialize the MFT LED
		changeLED = c.op("changeLED")
		try:
			changeLED.run(delayFrames=10)
			print("ran changeLED script onReplicate")
		except Exception as e:
			print("didn't run chopexec2")
			print("Error:",e)
		
		#c.par.clone = comp.par.master
		pass

	return
