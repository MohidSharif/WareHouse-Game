import pygame


class Actor:
    """
    Represents an Actor in the game. Can be the Player, a Monster, boxes, wall.
    Any object in the game's grid that appears on the stage, and has an
    x- and y-coordinate.
    """

    def __init__(self, icon_file, stage, x, y, delay=5):
        """
        (Actor, str, Stage, int, int, int) -> None
        Given the name of an icon file (with the image for this Actor),
        the stage on which this Actor should appear, the x- and y-coordinates
        that it should appear on, and the speed with which it should
        update, construct an Actor object.
        """

        self._icon = pygame.image.load(icon_file)  # the image image to display of self
        self.set_position(x, y)  # self's location on the stage
        self._stage = stage  # the stage that self is on

        # the following can be used to change this Actors 'speed' relative to other
        # actors speed. See the delay method.
        self._delay = delay
        self._delay_count = 0

    def set_position(self, x, y):
        """
        (Actor, int, int) -> None
        Set the position of this Actor to the given x- and y-coordinates.
        """

        (self._x, self._y) = (x, y)

    def get_position(self):
        """
        (Actor) -> tuple of two ints
        Return this Actor's x and y coordinates as a tuple.
        """

        return (self._x, self._y)

    def get_icon(self):
        """
        (Actor) -> pygame.Surface
        Return the image associated with this Actor.
        """

        return self._icon

    def is_dead(self):
        """
        (Actor) -> bool
        Return True iff this Actor is not alive.
        """

        return False

    def move(self, other, dx, dy):
        """
        (Actor, Actor, int, int) -> bool

        Other is an Actor telling us to move in direction (dx, dy). In this case, we just move.
        (dx,dy) is in {(1,1), (1,0), (1,-1), (0,1), (0,0), (0,-1), (-1,1), (-1,0), (-1,-1)}

        In the more general case, in subclasses, self will determine
        if they will listen to other, and if so, will try to move in
        the specified direction. If the target space is occupied, then we
        may have to ask the occupier to move.
        """

        self.set_position(self._x + dx, self._y + dy)
        return True

    def delay(self):
        """
        (Actor) -> bool
        Manage self's speed relative to other Actors.
        Each time we get a chance to take a step, we delay. If our count wraps around to 0
        then we actually do something. Otherwise, we simply return from the step method.
        """

        self._delay_count = (self._delay_count + 1) % self._delay
        return self._delay_count == 0

    def step(self):
        """
        (Actor) -> None
        Make the Actor take a single step in the animation of the game.
        self can ask the stage to help as well as ask other Actors
        to help us get our job done.
        """

        pass


class Player(Actor):
    """
    A Player is an Actor that can handle events. These typically come
    from the user, for example, key presses etc.
    """

    def __init__(self, icon_file, stage, x=0, y=0):
        """
        (Player, str, Stage, int, int) -> None
        Construct a Player with given image, on the given stage, at
        x- and y- position.
        """
        self.is_dead = False
        super().__init__(icon_file, stage, x, y)

    def handle_event(self, event):
        """
        Used to register the occurrence of an event with self.
        """

        self.quit()


class KeyboardPlayer(Player):
    """
    A KeyboardPlayer is a Player that can handle keypress events.
    """

    def __init__(self, icon_file, stage, x=0, y=0):
        """
        Construct a KeyboardPlayer. Other than the given Player information,
        a KeyboardPlayer also keeps track of the last key event that took place.
        """

        super().__init__(icon_file, stage, x, y)
        self._last_event = None  # we are only interested in the last event

    def handle_event(self, event):
        """
        (KeyboardPlayer, int) -> None
        Record the last event directed at this KeyboardPlayer.
        All previous events are ignored.
        """

        self._last_event = event

    def step(self):
        """
        (KeyboardPlayer) -> None
        Take a single step in the animation.
        For example: if the user asked us to move right, then we do that.
        """
        if 'Monster' in str(self):
            self.remove()

        if self._last_event is not None:
            dx, dy = None, None
            if self._last_event == pygame.K_s:  # Player moves DOWN with s key
                dx, dy = 0, 1
            if self._last_event == pygame.K_a:  # Player moves LEFT with a key
                dx, dy = -1, 0
            if self._last_event == pygame.K_d:  # Player moves RIGHT with d key
                dx, dy = 1, 0
            if self._last_event == pygame.K_w:  # Player moves UP with w key
                dx, dy = 0, -1
            if self._last_event == pygame.K_e:  # Player moves UP and RIGHT with key e
                dx, dy = 1, -1
            if self._last_event == pygame.K_q:  # Player moves UP and LEFT with key q
                dx, dy = -1, -1
            if self._last_event == pygame.K_x:  # Player moves DOWN and RIGHT with key x
                dx, dy = 1, 1
            if self._last_event == pygame.K_z:  # Player moves DOWN and LEFT with key z
                dx, dy = -1, 1
            if dx is not None and dy is not None:
                self.move(self, dx, dy)  # we are asking ourself to move

            self._last_event = None

    def move(self, other, dx, dy):
        """
        (Actor, Actor, int, int) -> bool
        Move this Actor by dx and dy, if possible. other is the Actor that asked to make this move.
        If a move is possible (a space is available) then move to it and return True.
        If another Actor is occupying that space, ask that Actor to move to make space, and then
        move to that spot, if possible.
        If a move is not possible, then return False.
        """
        act = True

        new_x = self._x + dx
        new_y = self._y + dy
        actor = self._stage.get_actor(new_x, new_y)

        if not self._stage.is_in_bounds(new_x, new_y) or 'Wall' in str(actor):
            return False

        if 'Player' in str(self) and 'Monster' in str(actor):
            self._stage.remove_player()

        if 'Box' in str(actor):
            act = actor.move(actor, dx, dy)

        if not act:
            return False
        else:
            return super().move(other, dx, dy)


class Box(Actor):
    """
    A Box Actor.
    """

    def __init__(self, icon_file, stage, x=0, y=0):
        """
        (Actor, str, Stage, int, int) -> None
        Construct a Box on the given stage, at given position.
        """

        super().__init__(icon_file, stage, x, y)

    def move(self, other, dx, dy):
        """
        (Actor, Actor, int, int) -> bool
        Move this Actor by dx and dy, if possible. other is the Actor that asked to make this move.
        If a move is possible (a space is available) then move to it and return True.
        If another Actor is occupying that space, ask that Actor to move to make space, and then
        move to that spot, if possible.
        If a move is not possible, then return False.
        """
        act = True

        new_x = self._x + dx
        new_y = self._y + dy

        actor = self._stage.get_actor(new_x, new_y)

        if not self._stage.is_in_bounds(new_x, new_y) or 'Wall' in str(actor) or 'Monster' in str(actor):
            return False

        if 'Box' in str(actor):
            act = actor.move(actor, dx, dy)

        if not act:
            return False
        else:
            return super().move(other, dx, dy)


class Sticky_Box(Actor):
    """
    A Box Actor.
    """

    def __init__(self, icon_file, stage, x=0, y=0):
        """
        (Actor, str, Stage, int, int) -> None
        Construct a Box on the given stage, at given position.
        """

        super().__init__(icon_file, stage, x, y)
        self._stuck = None

    def move(self, other, dx, dy):
        """
        (Actor, Actor, int, int) -> bool
        Move this Actor by dx and dy, if possible. other is the Actor that asked to make this move.
        If a move is possible (a space is available) then move to it and return True.
        If another Actor is occupying that space, ask that Actor to move to make space, and then
        move to that spot, if possible.
        If a move is not possible, then return False.
        """
        act = True

        new_x = self._x + dx
        new_y = self._y + dy

        actor = self._stage.get_actor(new_x, new_y)

        if not self._stage.is_in_bounds(new_x, new_y) or 'Wall' in str(actor) or 'Monster' in str(actor):
            if 'Monster' in str(actor):
                self._stuck = actor
                actor.is_stuck = True
            return False

        if self._stuck is not None:
            for act in self._stage._actors:
                if act == self._stuck:
                    act.is_stuck = False
            self._stuck = None

        if 'Box' in str(actor):
            act = actor.move(actor, dx, dy)

        if not act:
            return False
        else:
            return super().move(other, dx, dy)


class Wall(Actor):
    def __init__(self, icon_file, stage, x=0, y=0):
        """
        (Actor, str, Stage, int, int) -> None
        Construct a wall on the given stage, at given position.
        """

        super().__init__(icon_file, stage, x, y)


class Stage:
    """
    A Stage that holds all the game's Actors (Player, monsters, boxes, etc.).
    """

    def __init__(self, width, height, icon_dimension):
        '''Construct a Stage with the given dimensions.'''

        self._actors = []  # all actors on this stage (monsters, player, boxes, ...)
        self._player = None  # a special actor, the player

        # the logical width and height of the stage
        self._width, self._height = width, height

        self._icon_dimension = icon_dimension  # the pixel dimension of all actors
        # the pixel dimensions of the whole stage
        self._pixel_width = self._icon_dimension * self._width
        self._pixel_height = self._icon_dimension * self._height
        self._pixel_size = self._pixel_width, self._pixel_height

        # get a screen of the appropriate dimension to draw on
        self._screen = pygame.display.set_mode(self._pixel_size)

    def is_in_bounds(self, x, y):
        """
        (Stage, int, int) -> bool
        Return True iff the position (x, y) falls within the dimensions of this Stage."""

        return self.is_in_bounds_x(x) and self.is_in_bounds_y(y)

    def is_in_bounds_x(self, x):
        """
        (Stage, int) -> bool
        Return True iff the x-coordinate given falls within the width of this Stage.
        """

        return 0 <= x and x < self._width

    def is_in_bounds_y(self, y):
        """
        (Stage, int) -> bool
        Return True iff the y-coordinate given falls within the height of this Stage.
        """

        return 0 <= y and y < self._height

    def get_width(self):
        """
        (Stage) -> int
        Return width of Stage.
        """

        return self._width

    def get_height(self):
        """
        (Stage) -> int
        Return height of Stage.
        """

        return self._height

    def set_player(self, player):
        """
        (Stage, Player) -> None
        A Player is a special actor, store a reference to this Player in the attribute
        self._player, and add the Player to the list of Actors.
        """

        self._player = player
        self.add_actor(self._player)

    def remove_player(self):
        """
        (Stage) -> None
        Remove the Player from the Stage.
        """

        self.remove_actor(self._player)
        self._player = None

    def player_event(self, event):
        """
        (Stage, int) -> None
        Send a user event to the player (this is a special Actor).
        """

        self._player.handle_event(event)

    def add_actor(self, actor):
        """
        (Stage, Actor) -> None
        Add the given actor to the Stage.
        """

        self._actors.append(actor)

    def game_over_win(self):
        """
        (Stage) -> Bool
        Returns True if the game is over because the player
        has killed all the monsters
        """
        for item in self._actors:
            if 'Monster' in str(item):
                return False
        return True

    def game_over_lose(self):
        """
        (Stage) -> Bool
        Returns True if the game is over because the player
        has died
        """
        for item in self._actors:
            if 'Player' in str(item):
                return False
        return True

    def remove_actor(self, actor):
        """
        (Stage, Actor) -> None
        Remove the given actor from the Stage.
        """

        self._actors.remove(actor)

    def step(self):
        """
        (Stage) -> None
        Take one step in the animation of the game.
        Do this by asking each of the actors on this Stage to take a single step.
        """

        for a in self._actors:
            a.step()

    def get_actors(self):
        """
        (Stage) -> None
        Return the list of Actors on this Stage.
        """

        return self._actors

    def get_actor(self, x, y):
        """
        (Stage, int, int) -> Actor or None
        Return the first actor at coordinates (x,y).
        Or, return None if there is no Actor in that position.
        """

        for a in self._actors:
            if a.get_position() == (x, y):
                return a
        return None

    def draw(self):
        """
        (Stage) -> None
        Draw all Actors that are part of this Stage to the screen.
        """

        self._screen.fill((0, 0, 0))  # (0,0,0)=(r,g,b)=black
        for a in self._actors:
            icon = a.get_icon()
            (x, y) = a.get_position()
            d = self._icon_dimension
            rect = pygame.Rect(x * d, y * d, d, d)
            self._screen.blit(icon, rect)
        pygame.display.flip()


class Monster(Actor):
    """A Monster class."""

    def __init__(self, icon_file, stage, x=0, y=0, delay=5):
        '''Construct a Monster.'''

        super().__init__(icon_file, stage, x, y, delay)
        self.is_stuck = False
        self._dx = 1
        self._dy = 1

    def step(self):
        """
        Take one step in the animation (this Monster moves by one space).
        If it's being delayed, return None. Else, return True.
        """
        if not self.is_dead():
            if not self.delay(): return
            self.move(self, self._dx, self._dy)
            return True
        self._stage.remove_actor(self)

    def move(self, other, dx, dy):
        """
        (Actor, Actor, int, int) -> bool
        Move this Actor by dx and dy, if possible. other is the Actor that asked to make this move.
        If a move is possible (a space is available) then move to it and return True.
        If another Actor is occupying that space, or if that space is out of bounds,
        bounce back in the opposite direction.
        If a bounce back happened, then return False.
        """

        if self.is_stuck:
            return False

        if other != self:  # Noone pushes me around
            return False

        bounce_off_edge = False

        new_x = self._x + self._dx
        new_y = self._y + self._dy

        if not self._stage.is_in_bounds_x(new_x):
            self._dx = -self._dx
            bounce_off_edge = True

        if not self._stage.is_in_bounds_y(new_y):
            self._dy = - self._dy
            bounce_off_edge = True

        if bounce_off_edge:
            return False

        # FIX THIS FOR PART 3 OF THE LAB
        # MONSTERS SHOULD BOUNCE BACK FROM BOXES AND OTHER MONSTERS
        # HINT: actor = self._stage.get_actor(new_x,new_y)
        actor = self._stage.get_actor(new_x, new_y)
        if actor is not None:
            self._dx = - self._dx
            self._dy = - self._dy
        if 'Box' in str(actor) or 'Monster' in str(actor) or 'Wall' in str(actor):
            if 'Sticky_Box' in str(actor):
                actor._stuck = self
                self.is_stuck = True
            return False

        if 'Player' in str(actor):
            self._stage.remove_player()

        return super().move(other, dx, dy)

    def is_dead(self):
        """
        Return whether this Monster has died.
        That is, if self is surrounded on all sides, by either Boxes or
        other Monsters."""

        d_dx, d_dy = 0, 1
        l_dx, l_dy = -1, 0
        r_dx, r_dy = 1, 0
        u_dx, u_dy = 0, -1
        ur_dx, ur_dy = 1, -1
        ul_dx, ul_dy = -1, -1
        dr_dx, dr_dy = 1, 1
        dl_dx, dl_dy = -1, 1

        d_actor = self._stage.get_actor(self._x + d_dx, self._y + d_dy)
        l_actor = self._stage.get_actor(self._x + l_dx, self._y + l_dy)
        r_actor = self._stage.get_actor(self._x + r_dx, self._y + r_dy)
        u_actor = self._stage.get_actor(self._x + u_dx, self._y + u_dy)
        ur_actor = self._stage.get_actor(self._x + ur_dx, self._y + ur_dy)
        ul_actor = self._stage.get_actor(self._x + ul_dx, self._y + ul_dy)
        dr_actor = self._stage.get_actor(self._x + dr_dx, self._y + dr_dy)
        dl_actor = self._stage.get_actor(self._x + dl_dx, self._y + dl_dy)

        if (d_actor is None or 'Player' in str(d_actor)) and self._stage.is_in_bounds_y(self._y + d_dy):
            return False
        if (u_actor is None or 'Player' in str(u_actor)) and self._stage.is_in_bounds_y(self._y + u_dy):
            return False
        if (l_actor is None or 'Player' in str(l_actor)) and self._stage.is_in_bounds_x(self._x + l_dx):
            return False
        if (r_actor is None or 'Player' in str(r_actor)) and self._stage.is_in_bounds_x(self._x + r_dx):
            return False
        if (ur_actor is None or 'Player' in str(ur_actor)) and self._stage.is_in_bounds(self._x + ur_dx,
                                                                                        self._y + ur_dy):
            return False
        if (ul_actor is None or 'Player' in str(ul_actor)) and self._stage.is_in_bounds(self._x + ul_dx,
                                                                                        self._y + ul_dy):
            return False
        if (dr_actor is None or 'Player' in str(dr_actor)) and self._stage.is_in_bounds(self._x + dr_dx,
                                                                                        self._y + dr_dy):
            return False
        if (dl_actor is None or 'Player' in str(dl_actor)) and self._stage.is_in_bounds(self._x + dl_dx,
                                                                                        self._y + dl_dy):
            return False

        return True
