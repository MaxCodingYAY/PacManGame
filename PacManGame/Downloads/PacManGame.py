import arcade

# Constants
TILE_SCALING = 0.5
PLAYER_SCALING = 0.5
SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 1000
SCREEN_TITLE = "Multiplayer Pacman"
MOVEMENT_SPEED = 3
SPRITE_PIXEL_SIZE = 60
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING


class PacmanGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        # Map
        self.tile_map = None

        # Sprites
        self.wall_list = None
        self.coin_list = None
        self.player1 = None
        self.player2 = None

        self.score1 = 0
        self.score2 = 0

        self.physics_engine = None
        self.end_of_map = 0
        self.game_over = False
        self.end_of_map = 0

        self.gui_camera = None
        self.camera = None

        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        self.camera = arcade.Camera(self.width, self.height)
        self.gui_camera = arcade.Camera(self.width, self.height)

        # Initialize the players
        self.player1 = arcade.Sprite("PCT.png", 0.1)
        self.player1.center_x = 100
        self.player1.center_y = 100
        
        self.player2 = arcade.Sprite("PCT2.png", 0.1)
        self.player2.center_x = 200
        self.player2.center_y = 100


        # Load the tile map
        map_name = "Truepacman Map.json"
        layer_options = {
            "Walls": {"use_spatial_hash": True},
            "Coins": {"use_spatial_hash": True},
        }
        self.tile_map = arcade.load_tilemap(map_name, scaling=TILE_SCALING)
        self.end_of_map = self.tile_map.width * GRID_PIXEL_SIZE

        self.wall_list = self.tile_map.sprite_lists["Walls"]
        self.coin_list = self.tile_map.sprite_lists["Coins"]

        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)

        walls = [self.wall_list, ]
        self.physics_engine1 = arcade.PhysicsEnginePlatformer(self.player1, walls)
        self.physics_engine2 = arcade.PhysicsEnginePlatformer(self.player2, walls)

        # # Manually set hit boxes for player sprites
        # self.player1.set_hit_box([[0, 0], [self.player1.width, 0], [self.player1.width, self.player1.height], [0, self.player1.height]])
        # self.player2.set_hit_box([[0, 0], [self.player2.width, 0], [self.player2.width, self.player2.height], [0, self.player2.height]])

        # Manually set hit boxes for coin sprites based on texture size
        # for coin in self.coin_list:
        #     if coin.texture is not None:  # Check if texture is not None
                    # coin.set_hit_box([[0, 0], [coin.texture.width, 0], [coin.texture.width, coin.texture.height], [0, coin.texture.height]])

        self.game_over = False

    def on_draw(self):
        arcade.start_render()

        # # Draw the tile map layers
        # for layer_name, layer in self.tile_map.layers.items():
        #     if layer_name != "Coins":  # Exclude coin layer for now
        #         layer.draw()

    # Draw the sprites
        self.player1.draw()
        self.player2.draw()
        self.coin_list.draw()

        # Draw the scores
        arcade.draw_text(f"Player 1 Score: {self.score1}", 10, 20, arcade.color.WHITE, 14)
        arcade.draw_text(f"Player 2 Score: {self.score2}", 10, 40, arcade.color.WHITE, 14)


            # Draw the sprites
        self.player1.draw()
        self.player2.draw()
        self.coin_list.draw()

        # Draw the scores
        arcade.draw_text(f"Player 1 Score: {self.score1}", 10, 20, arcade.color.WHITE, 14)
        arcade.draw_text(f"Player 2 Score: {self.score2}", 10, 40, arcade.color.WHITE, 14)


    def on_key_press(self, key, modifiers):
        # Player 1 controls
        if key == arcade.key.W:
            self.player1.change_y = MOVEMENT_SPEED
        elif key == arcade.key.S:
            self.player1.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.A:
            self.player1.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.D:
            self.player1.change_x = MOVEMENT_SPEED

        # Player 2 controls
        if key == arcade.key.UP:
            self.player2.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player2.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player2.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player2.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        # Player 1 controls
        if key in [arcade.key.W, arcade.key.S]:
            self.player1.change_y = 0
        elif key in [arcade.key.A, arcade.key.D]:
            self.player1.change_x = 0

        # Player 2 controls
        if key in [arcade.key.UP, arcade.key.DOWN]:
            self.player2.change_y = 0
        elif key in [arcade.key.LEFT, arcade.key.RIGHT]:
            self.player2.change_x = 0

    def check_wall_collision(self, player):
        """Check if the player collides with a wall."""
        return arcade.check_for_collision_with_list(player, self.wall_list)

    def on_update(self, delta_time):
        # Move player 1
        self.player1.update()  # Use self.player1 instead of self.player1_sprite
        # if self.check_wall_collision(self.player1):
        #     self.player1.center_x -= self.player1.change_x
        #     self.player1.center_y -= self.player1.change_y

        # Move player 2
        self.player2.update()  # Use self.player2 instead of self.player2_sprite
        # if self.check_wall_collision(self.player2):
        #     self.player2.center_x -= self.player2.change_x
        #     self.player2.center_y -= self.player2.change_y

        # Check for collisions with coins
        # coin_hit_list1 = arcade.check_for_collision_with_list(self.player1, self.coin_list)
        # coin_hit_list2 = arcade.check_for_collision_with_list(self.player2, self.coin_list)

        # for coin in coin_hit_list1:
        #     coin.remove_from_sprite_lists()
        #     self.score1 += 1

        # for coin in coin_hit_list2:
        #     coin.remove_from_sprite_lists()
        #     self.score2 += 1


def main():
    game = PacmanGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
