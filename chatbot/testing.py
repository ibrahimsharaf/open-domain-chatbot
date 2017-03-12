from load_cornell import CornellData

C = CornellData('/home/ibrahimsharaf/workspace/ChatbotGP/data/cornell/')
conv = C.getConversations()
for i in range(10):
    print conv[i]

