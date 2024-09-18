
class Math():
  def Mean(analisysData:list):
    srednia = 0
    srednia = sum(analisysData)
    return srednia/len(analisysData)
  def Difference(a, b):
    difference = b/a
    difference = difference*100
    return difference-100
  def Normalize(analisysData:list, normalizeNumber:int):
    najwieksza = 0
    for element in analisysData:
      if element > najwieksza:
        najwieksza = element
    position = 0
    for position in range(len(analisysData)):
      analisysData[position] = analisysData[position]/(najwieksza/normalizeNumber)
    return analisysData
  def MakeInt(value:float, divideNumber:int):
    return round(value-divideNumber,0)
  def AbsoluteDifference(a,b):
    return abs(a-b)
  def AbsoluteIntPercentDifference(a, b):
    return abs(Math.MakeInt(Math.Difference(a,b)))
  def WeightedAverage(analisysData=[],weights=[]):
    score=[]
    for position in range(len(analisysData)):
      for weight in range(weights[position]):
        analisysData.insert(analisysData[position]+weight, analisysData[position])
    return sum(analisysData)/len(analisysData)
  def NumberRepeat(numbers:list) -> dict:
        nums = {}
        for liczba in range(len(numbers)):
            if numbers[liczba] in nums:
                nums[numbers[liczba]] +=1
            else:
               nums[numbers[liczba]] = 1
        

        return nums
     
class Finance():
    
    def FinancialAngle(amounts:list, max_change:int):
        angles = []
        for i in range(1, len(amounts)):
            start_amount = amounts[i - 1]
            end_amount = amounts[i]
            angle = 180 * ((end_amount - start_amount) / max_change)
            angles.append(max(0, min(angle, 180)))
        return angles
    def FinanceChance(numbers:list) -> dict:
        chance = {}
        repeats = Math.NumberRepeat(numbers)
        suma = sum(repeats.values())
        for i in range(len(numbers)):
           if numbers[i] not in chance:
            chance[numbers[i]] = (repeats.get(numbers[i])/suma)*100
        return chance
    

    



