import OzEngine as oz
import os

class Coin(oz.Sprite):

  __slots__ = "canvas_owner", "char", "position", "name", "group", "distance",
  "on_function_ready"

  def __init__(
    self,
    canvas_owner: object,
    char: str,
    position: list,
    name: str,
    group=None,
  ):
    '''Character that represents the sprite when rendered.'''
    self.char = char
    '''List that has two element "x" and "y" it tells where to render the sprite.'''
    self.position = position
    '''Name of the sprite that can be used to get reference from it using the "get_sprite" method throught a "Canvas" object.'''
    self.name = name
    '''Canvas that the sprite is associated to.'''
    self.canvas_owner = canvas_owner
    '''group is a string that be used to call a method on each sprite that has the same method with 
    the method "call_group" through the canvas and it can also be used to check collision by seing which sprite of which
    group is colliding with our sprite with the method "get_colliding_groups" that can be executed by a "Sprite" object. '''
    self.group = group

    if name in canvas_owner.sprite_names:
      # change name if already taken
      self.name = name + f"@{str(id(self))}"

    # register infos in "canvas_owner" :
    canvas_owner.sprite_tree.append(self)
    canvas_owner.sprite_names.append(self.name)
    canvas_owner.sprite_names_dict[self.name] = self
    canvas_owner.sprite_position_dict[self] = position

    if not (group in canvas_owner.sprite_group_dict):
      #if group is new then add to "group_tree" and create new key
      #location for "sprite_group_dict".
      canvas_owner.sprite_group_dict[group] = []
      canvas_owner.group_tree.append(group)

    canvas_owner.sprite_group_dict[group].append(self)

    if self.char == "🟡":
      coin_yellow_position.append(self.position)
    else:
      coin_red_position.append(self.position)


def place_coin(x, val):

  coin = Coin(canvas, val, [x, coin_level[x]], "coin")
  coin_level[x] -= 1


def get_possible_input():

  return [str(c) for c in range(len(coin_level)) if not (coin_level[c] == -1)]


def check_aligned():


  has_alignement = (False , "None")
  
  # check if red are aligned
  for red_coin_pos in coin_red_position:

    horizontal_match = 0
    vertical_match = 0
    diagonal_left_match = 0
    diagonal_right_match = 0

    POS_X = red_coin_pos[0]
    POS_Y = red_coin_pos[1]

    # horizontal_match check
    match_coin = []
    for i in range(1, 4):
      if [i + POS_X ,POS_Y] in coin_red_position:
        horizontal_match += 1
        

      else:
        break

    if horizontal_match == 3:
      has_alignement = (True , "red")
      break


    # vertical_match check
    for i in range(1, 4):
      if [POS_X, i + POS_Y] in coin_red_position:
        vertical_match += 1

      else:
        break

    if vertical_match == 3:
      has_alignement = (True , "red")
      break

    
    # diagonal_left_match check
    for i in range(1, 4):
      if [-i + POS_X, -i + POS_Y] in coin_red_position:
        diagonal_left_match += 1

      else:
        break

    if diagonal_left_match == 3:
      has_alignement = (True , "red")
      break

    # diagonal_right_match check
    for i in range(1, 4):
      if [i + POS_X, -i + POS_Y] in coin_yellow_position:
        diagonal_right_match += 1

      else:
        break

    if diagonal_right_match == 3:
      has_alignement = (True , "red")
      break
  
  if has_alignement[1] != "None":
    return has_alignement
  
  for yellow_coin_pos in coin_yellow_position:

    POS_X = yellow_coin_pos[0]
    POS_Y = yellow_coin_pos[1]

    horizontal_match = 0
    vertical_match = 0
    diagonal_left_match = 0
    diagonal_right_match = 0

    # horizontal_match check
    for i in range(1, 4):
      if [i + POS_X ,POS_Y] in coin_yellow_position:
        horizontal_match += 1

      else:
        break

    if horizontal_match == 3:
      has_alignement = True
      break


    # vertical_match check
    for i in range(1, 4):
      if [POS_X, i + POS_Y] in coin_yellow_position:
        vertical_match += 1

      else:
        break

    if vertical_match == 3:
      has_alignement = (True , "yellow")
      break

    
    # diagonal_left_match check
    for i in range(1, 4):
      if [-i + POS_X, -i + POS_Y] in coin_yellow_position:
        diagonal_left_match += 1

      else:
        break

    if diagonal_left_match == 3:
      has_alignement = (True , "yellow")
      break

    # diagonal_right_match check
    for i in range(1, 4):
      if [i + POS_X, -i + POS_Y] in coin_yellow_position:
        diagonal_right_match += 1

      else:
        break

    if diagonal_right_match == 3:
      has_alignement = (True , "yellow")
      break

  return has_alignement

def game():

  global canvas
  global coin_red_position
  global coin_yellow_position
  global coin_level
  
  canvas = oz.Canvas("██")
  camera = oz.Camera(canvas, [7, 6], [0, 0], "cam")

  coin_level = [5 for i in range(camera.size[0])]
  coin_red_position = []
  coin_yellow_position = []

  is_turn_p_one = True
  print(camera.render())
  print( " " + (" ".join(get_possible_input())))

  while True:

    action = input(": ")

    if action in get_possible_input():
    
      place_coin(int(action), "🔴" if is_turn_p_one else "🟡") 
      is_turn_p_one = not is_turn_p_one

      is_aligned = check_aligned()


      if is_aligned[0]:

        break
    
    os.system('cls')
    print(camera.render())
    print( " " + (" ".join(get_possible_input())))
    
  os.system('cls')
  print(camera.render())
  print(f"Aligned ! {is_aligned[1]} won !")
  if input("Would you like to play an other round ?(y/n): ") == "y":
    game()
  else:
    exit()

game()
