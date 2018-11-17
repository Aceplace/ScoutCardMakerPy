from enum import Enum

class Direction(Enum):
    LEFT = 1
    RIGHT = 2
    STR = 3
    WK = 4

class StrengthType(Enum):
    ATTACHED = 1
    RECEIVER_STRENGTH = 2

ATTACH_DISTANCE = 6
GHOST_DISTANCE = 4

def get_align_side(direction, strength_type, formation):
    if direction == Direction.LEFT or direction == Direction.RIGHT:
        return direction

    if strength_type == StrengthType.ATTACHED:
        strength_direction = get_attached_receiver_strength(formation)
    else:
        strength_direction = get_receiver_strength(formation)

    if strength_direction == 'LT':
        if direction == Direction.STR:
            return Direction.LEFT
        else:
            return Direction.RIGHT
    else:
        if direction == Direction.STR:
            return Direction.RIGHT
        else:
            return Direction.LEFT

def get_receiver_strength(formation, default_strength='RT'):
    #first check for strength is absolute number of receivers (defined as outside the tackle)
    receivers_to_left_of_lt = [player for label, player in formation.players.items() if player.x < formation.lt.x]
    receivers_to_right_of_rt = [player for label, player in formation.players.items() if player.x > formation.rt.x]

    if len(receivers_to_left_of_lt) > len(receivers_to_right_of_rt):
        return 'LT'
    if len(receivers_to_left_of_lt) < len(receivers_to_right_of_rt):
        return 'RT'

    #next check is if one side has more detached receivers then the other side
    attached_receivers_to_left = get_number_of_attached_receivers(formation, 'LT')
    attached_receivers_to_right = get_number_of_attached_receivers(formation, 'RT')

    if attached_receivers_to_left < attached_receivers_to_right:
        return 'LT'
    if attached_receivers_to_left > attached_receivers_to_right:
        return 'RT'

    #next is to consider backfield
    offset_backs_to_left = get_number_of_offset_backs(formation, 'LT')
    offset_back_to_right = get_number_of_offset_backs(formation, 'RT')

    if offset_backs_to_left > offset_back_to_right:
        return 'LT'
    if offset_backs_to_left < offset_back_to_right:
        return 'RT'

    return default_strength


def get_attached_receiver_strength(formation, default_strength='RT'):
    attached_receivers_to_left = get_number_of_attached_receivers(formation, 'LT')
    attached_receivers_to_right = get_number_of_attached_receivers(formation, 'RT')

    if attached_receivers_to_left > attached_receivers_to_right:
        return 'LT'
    if attached_receivers_to_left < attached_receivers_to_right:
        return 'RT'

    return get_receiver_strength(formation, default_strength)

def get_number_of_receivers(formation, direction):
    if direction == 'LT':
        return len([player for label, player in formation.players.items() if player.x < formation.lt.x])
    elif direction == 'RT':
        return len([player for label, player in formation.players.items() if player.x > formation.rt.x])

def get_number_of_attached_receivers(formation, direction):
    number_of_attached_receivers = 0

    if direction == 'LT':
        sorted_receivers_outside_tackle = list(sorted([player for label, player in formation.players.items() if player.x < formation.lt.x], key=lambda player: player.x))
        sorted_receivers_outside_tackle.reverse()
        outside_most_attached_player = formation.lt
    else:
        sorted_receivers_outside_tackle = list(sorted([player for label, player in formation.players.items() if player.x > formation.rt.x], key=lambda player: player.x))
        outside_most_attached_player = formation.rt

    for player in sorted_receivers_outside_tackle:
        if abs(player.x - outside_most_attached_player.x) <= ATTACH_DISTANCE:
            number_of_attached_receivers += 1
            outside_most_attached_player = player

    return number_of_attached_receivers


def get_number_of_offset_backs(formation, direction):
    number_of_attached_receivers = 0
    if direction == 'LT':
        return len([player for label, player in formation.players.items() if player.x >= formation.lt.x and player.x < 0])
    else:
        return len([player for label, player in formation.players.items() if player.x <= formation.rt.x and player.x > 0])


def get_first_attached(formation, direction):
    if direction == 'LT':
        sorted_receivers_outside_tackle = list(
            sorted([player for label, player in formation.players.items() if player.x < formation.lt.x],
                   key=lambda player: player.x))
        sorted_receivers_outside_tackle.reverse()
        outside_most_attached_player = formation.lt
    else:
        sorted_receivers_outside_tackle = list(
            sorted([player for label, player in formation.players.items() if player.x > formation.rt.x],
                   key=lambda player: player.x))
        outside_most_attached_player = formation.rt

    for player in sorted_receivers_outside_tackle:
        if abs(player.x - outside_most_attached_player.x) <= ATTACH_DISTANCE:
            return player

    return None


def get_second_attached(formation, direction):
    number_of_attached_receivers = 0

    if direction == 'LT':
        sorted_receivers_outside_tackle = list(
            sorted([player for label, player in formation.players.items() if player.x < formation.lt.x],
                   key=lambda player: player.x))
        sorted_receivers_outside_tackle.reverse()
        outside_most_attached_player = formation.lt
    else:
        sorted_receivers_outside_tackle = list(
            sorted([player for label, player in formation.players.items() if player.x > formation.rt.x],
                   key=lambda player: player.x))
        outside_most_attached_player = formation.rt

    for player in sorted_receivers_outside_tackle:
        if abs(player.x - outside_most_attached_player.x) <= ATTACH_DISTANCE:
            number_of_attached_receivers += 1
            if (number_of_attached_receivers == 2):
                return player
            outside_most_attached_player = player

    return None


def get_receivers_outside_across(formation, direction):
    if formation.q.x != 0:
        receivers = [player for label, player in formation.players.items() if label in ['T', 'H', 'X', 'Y', 'Z', 'Q']]
    else:
        receivers = [player for label, player in formation.players.items() if label in ['T', 'H', 'X', 'Y', 'Z']]

    if direction == 'LT':
        receivers.sort(key = lambda player: (player.x, player.y))
    else:
        receivers.sort(key = lambda player: (-1 * player.x, player.y))

    return receivers

def get_receivers_outside_in(formation, direction):
    if formation.q.x != 0:
        receivers = [player for label, player in formation.players.items() if label in ['T', 'H', 'X', 'Y', 'Z', 'Q']]
    else:
        receivers = [player for label, player in formation.players.items() if label in ['T', 'H', 'X', 'Y', 'Z']]

    if direction == 'LT':
        receivers.sort(key = lambda player: (player.x, player.y))
        filtered_receivers = [receiver for receiver in receivers if receiver.x < formation.lt.x]
    else:
        receivers.sort(key = lambda player: (-1 * player.x, player.y))
        filtered_receivers = [receiver for receiver in receivers if receiver.x > formation.rt.x]

    return filtered_receivers

def get_receivers_inside_out(formation, direction):
    if formation.q.x != 0:
        receivers = [player for label, player in formation.players.items() if label in ['T', 'H', 'X', 'Y', 'Z', 'Q']]
    else:
        receivers = [player for label, player in formation.players.items() if label in ['T', 'H', 'X', 'Y', 'Z']]

    if direction == 'LT':
        receivers.sort(key = lambda player: (-1 * player.x, player.y))
        filtered_receivers = [receiver for receiver in receivers if receiver.x < formation.lt.x]
    else:
        receivers.sort(key = lambda player: (player.x, player.y))
        filtered_receivers = [receiver for receiver in receivers if receiver.x > formation.rt.x]

    return filtered_receivers


def get_formation_structure(formation):
    receivers_to_left = get_number_of_receivers(formation, 'LT')
    receivers_to_right = get_number_of_receivers(formation, 'RT')
    if receivers_to_left == 1 and receivers_to_right == 1:
        return '1x1'
    if (receivers_to_left == 1 and receivers_to_right == 2) or (receivers_to_left == 2 and receivers_to_right == 1):
        return '2x1'
    if receivers_to_left == 2 and receivers_to_right == 2:
        return '2x2'
    if (receivers_to_left == 3 and receivers_to_right == 1) or (receivers_to_left == 1 and receivers_to_right == 3):
        return '3x1'
    if (receivers_to_left == 3 and receivers_to_right == 2) or (receivers_to_left == 2 and receivers_to_right == 3):
        return '3x2'
    return '4x1'



def get_surface_structures(formation, direction):
    surface_structure = []
    number_of_receivers = get_number_of_receivers(formation, direction)
    number_of_attached_receivers = get_number_of_attached_receivers(formation, direction)
    if number_of_receivers == 0:
        surface_structure.append('Zero Receivers')
    elif number_of_receivers == 1:
        surface_structure.append('One Receiver')
    elif number_of_receivers == 2:
        surface_structure.append('Two Receivers')
    elif number_of_receivers == 3:
        surface_structure.append('Three Receivers')
    elif number_of_receivers == 4:
        surface_structure.append('Four Receivers')
    elif number_of_receivers == 5:
        surface_structure.append('Five Receivers')

    if number_of_receivers == 1 and number_of_attached_receivers == 1:
        surface_structure.append('Nub')
    if number_of_receivers == 1 and number_of_attached_receivers == 0:
        surface_structure.append('Split')

    if number_of_receivers == 2 and number_of_attached_receivers == 0:
        surface_structure.append('Twin')
    if number_of_receivers == 2 and number_of_attached_receivers == 1:
        surface_structure.append('Pro')
    if number_of_receivers == 2 and number_of_attached_receivers == 2:
        surface_structure.append('Wing')

    if number_of_receivers == 3 and number_of_attached_receivers == 0:
        surface_structure.append('Trips')
    if number_of_receivers == 3 and number_of_attached_receivers == 1:
        surface_structure.append('Indy')
    if number_of_receivers == 3 and number_of_attached_receivers == 2:
        surface_structure.append('Indy Wing')
    if number_of_receivers == 3 and number_of_attached_receivers == 3:
        surface_structure.append('Tight Bunch')

    return surface_structure

