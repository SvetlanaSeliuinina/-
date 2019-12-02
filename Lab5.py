from web3 import Web3
import statistics
import matplotlib.pyplot as plt
import numpy

K = 53
block = 8961400
start = block - 1000*(K-1)

web3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/46f7d1163f3e427d87ac0aae543ed880"))

Blocks = []
Percent = []
Commisions = []
Rewards = []
Contracts = 0

for i in range(1001):
    print(i)
    x = i + start
    block = web3.eth.getBlock(x)
    allcom = 0
    for y in block.transactions:
        trans = web3.eth.getTransaction(y.hex())
        transRec = web3.eth.getTransactionReceipt(y.hex())
        allcom += (float(transRec.gasUsed)*float(trans.gasPrice)/(10**18))
        if trans.input != '0x': Contracts += 1
    if len(block.transactions)==0: blockReward=2
    else: blockReward = 2 + allcom

    Blocks.append(i)
    Commisions.append(allcom)
    Rewards.append(blockReward)
    Percent.append(allcom/blockReward*100)

MatExp = statistics.mean(Commisions)
Median = statistics.median(Commisions)
Range = max(Commisions) - min(Commisions)
Deviation = numpy.std(Commisions)
Dispersion = numpy.var(Commisions)

file = open('lab5.txt', 'w')
file.write("Мат. ожидание комиссии = " + str(MatExp))
file.write("Медиана комиссии = " + str(Median))
file.write("Размах комиссии = "+ str(Range))
file.write("Ср. кв. отклонение комиссии = "+ str(Deviation))
file.write("Дисперсия комиссии = " + str(Dispersion))
file.write("Количество обращений к смарт контрактам = " + str(Contracts))
file.close()

#fig, axs = plt.subplots(1, 2, figsize=(8, 8), sharey=False)
fig, axs = plt.subplots(1, 2, figsize=(8, 4), sharey=False)
axs[0].scatter(Blocks, Percent)
axs[0].set_title('Комиссия по блокам в процентах')
axs[0].set_xlabel('Номера блоков')
axs[0].set_ylabel('Комиссия, %')
axs[1].scatter(Blocks, Commisions)
axs[1].set_title('Комисссия по блокам в абсолютных величинах')
axs[1].set_xlabel('Номера блоков')
axs[1].set_ylabel('Комиссия, Eth')
fig.subplots_adjust(left=0.08, right=0.92, bottom=0.15, top=0.9, hspace=0.3, wspace=0.3)
plt.show()