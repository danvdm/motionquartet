# dot positions (x, y)
bottom_right = [1, -1]
top_right = [1, 1]
top_left = [-1, 1]
bottom_left = [-1, -1]
bottom_middle = [0, 1]
left_middle = [1, 0]
top_middle = [0, -1]
right_middle = [-1, 0]

# slide setup (list of lists with indices of positions displayed per frame - could probably be coded better)

two_by_two = [[0, 1], [2, 3]] # normal two dots at a time in order of list
four_by_one = [[0], [1], [2], [3]] # normal two dots at a time in order of list
one_by_four = [[0, 1, 2, 3]] # normal two dots at a time in order of list
one_by_four_check = [[0, 0, 0, 0]] # normal two dots at a time in order of list

diagonal = two_by_two,  [top_left, 
                        bottom_right,  
                        bottom_left, 
                        top_right]  

horizontal = two_by_two,    [top_left, 
                            bottom_left,  
                            bottom_right, 
                            top_right]  

vertical = two_by_two,  [top_left, 
                        top_right,  
                        bottom_left, 
                        bottom_right]  

circular_clockwise_4 = four_by_one, [top_left,
                                    top_right, 
                                    bottom_right, 
                                    bottom_left]  

check = four_by_one,  [bottom_left,
                        bottom_left, 
                        bottom_left, 
                        bottom_right]  


configuration = {"diagonal":diagonal, 
                 "horizontal":horizontal, 
                 "vertical":vertical, 
                 "circular_clockwise_4":circular_clockwise_4, 
                 "check":check}