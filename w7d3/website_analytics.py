monday_visitors = {"user1", "user2", "user3", "user4", "user5"}
tuesday_visitors = {"user2", "user4", "user6", "user7", "user8"}
wednesday_visitors = {"user1", "user3", "user6", "user9", "user10"}

all_unique_visitors = monday_visitors | tuesday_visitors | wednesday_visitors
print(len(all_unique_visitors))
print(all_unique_visitors)

returning_tuesday = monday_visitors & tuesday_visitors
print(returning_tuesday)

new_monday = monday_visitors
new_tuesday = tuesday_visitors - monday_visitors
new_wednesday = wednesday_visitors - (monday_visitors | tuesday_visitors)
print( new_monday)
print(new_tuesday)
print(new_wednesday)

loyal_visitors = monday_visitors & tuesday_visitors & wednesday_visitors
print( loyal_visitors)

overlap_mon_tue = monday_visitors & tuesday_visitors
overlap_tue_wed = tuesday_visitors & wednesday_visitors
overlap_mon_wed = monday_visitors & wednesday_visitors
print( overlap_mon_tue)
print( overlap_tue_wed)
print( overlap_mon_wed)
