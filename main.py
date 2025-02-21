import multimodal
import snap

#Ablauf nicht optimal, da erst multimodal.vision() aufgerufen wird und dann snap.screencapture()
snap.screencapture()
print(multimodal.vision())