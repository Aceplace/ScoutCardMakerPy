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


def get_receivers_outside_in(formation, direction):
    if formation.q.x != 0:
        receivers = [player for label, player in formation.players.items() if label in ['T', 'H', 'X', 'Y', 'Z', 'Q']]
    else:
        receivers = [player for label, player in formation.players.items() if label in ['T', 'H', 'X', 'Y', 'Z']]

    if direction == 'LT':
        receivers.sort(key = lambda player: (player.x, player.y))
    else:
        receivers.sort(key = lambda player: (-1*player.x, player.y))

    return receivers


from offensiveformation.formation import Formation

if __name__=='__main__':
    formation = Formation()
    formation.h.x = -26
    formation.y.x = 12
    formation.t.x = -4
    print(get_attached_receiver_strength(formation))
