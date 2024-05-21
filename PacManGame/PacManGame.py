import arcade
import arcade.gui

# Constants
TILE_SCALING = 1
PLAYER_SCALING = 1
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 920
SCREEN_TITLE = "Multiplayer Pacman"
MOVEMENT_SPEED = 2.3
MOVEMENT_SPEED2 = 2.5
SPRITE_PIXEL_SIZE = 60
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING
MAX_LEVEL = 3


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
        
        self.player2_frozen = False

        self.game_over = False

        
        arcade.set_background_color(arcade.color.BLACK)
        

    def setup(self, level):
        self.camera = arcade.Camera(self.width, self.height)
        self.gui_camera = arcade.Camera(self.width, self.height)

        # Initialize the players
        if level == 1:
            self.player1 = arcade.Sprite("PCT.png", 0.11)
            self.player1.center_x = 100
            self.player1.center_y = 480

            self.player2 = arcade.Sprite("PCT2.png", 0.04)
            self.player2.center_x = 1000
            self.player2.center_y = 480
        elif level == 2:
            self.player1 = arcade.Sprite("PCT.png", 0.11)
            self.player1.center_x = 140
            self.player1.center_y = 600

            self.player2 = arcade.Sprite("PCT2.png", 0.04)
            self.player2.center_x = 960
            self.player2.center_y = 600
        else:
            self.player1 = arcade.Sprite("PCT.png", 0.11)
            self.player1.center_x = 100
            self.player1.center_y = 640

            self.player2 = arcade.Sprite("PCT2.png", 0.04)
            self.player2.center_x = 1000
            self.player2.center_y = 640
            

        # Load the tile map
        map_name = "Truepacman Map.json"
        if level == 2:
            map_name = "Truesnow Map.json"
        if level == 3:
            map_name = "Skyrealm Map.json"
        map_filename = self.get_map_filename(level)
        layer_options = {
            "Walls": {"use_spatial_hash": True},
            "Coins": {"use_spatial_hash": True},
        }
        if level == 2:
            layer_options = {
                "Walls2": {"use_spatial_hash": True},
                "Coins2": {"use_spatial_hash": True},
            }
        if level == 3:
            layer_options = {
                "Walls3": {"use_spatial_hash": True},
                "Coins3": {"use_spatial_hash": True},
            }
          
        self.tile_map = arcade.load_tilemap(map_name, scaling=TILE_SCALING)
        self.end_of_map = self.tile_map.width * GRID_PIXEL_SIZE

        if level == 1:
            self.wall_list = self.tile_map.sprite_lists["Walls"]
            self.coin_list = self.tile_map.sprite_lists["Coins"]
            self.powerup_list = self.tile_map.sprite_lists.get("Powerups", None)
        elif level == 2:
            self.wall_list = self.tile_map.sprite_lists["Walls2"]
            self.coin_list = self.tile_map.sprite_lists["Coins2"]
            self.powerup_list = self.tile_map.sprite_lists.get("Powerups2", None)
        else:
            self.wall_list = self.tile_map.sprite_lists["Walls3"]
            self.coin_list = self.tile_map.sprite_lists["Coins3"]
            self.powerup_list = self.tile_map.sprite_lists.get("Powerups3", None)

        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)

        walls = [self.wall_list, ]
        self.physics_engine1 = arcade.PhysicsEngineSimple(self.player1, walls)
        self.physics_engine2 = arcade.PhysicsEngineSimple(self.player2, walls)

    def get_map_filename(self, level):
        # Define the mapping between level numbers and map filenames
        map_filenames = {
            1: "Truepacman Map.json",
            2: "Truesnow Map.json",
            3: "Skyrealm Map.json"
        }
        # Return the map filename corresponding to the given level
        return map_filenames.get(level, "Truepacman Map.json")  # Use a default map if level not found

    def on_draw(self):
        arcade.start_render()     

        if self.current_level == 1:
            arcade.set_background_color(arcade.color.BLACK)
        elif self.current_level == 2:
            arcade.set_background_color(arcade.color.ASH_GREY)
        else:
            arcade.set_background_color(arcade.color.BLIZZARD_BLUE) 
        # Draw the sprites, walls, and scores
        self.player1.draw()
        self.player2.draw()
        self.wall_list.draw()
        self.coin_list.draw()
        self.powerup_list.draw()
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
            self.player2.change_y = MOVEMENT_SPEED2
        elif key == arcade.key.DOWN:
            self.player2.change_y = -MOVEMENT_SPEED2
        elif key == arcade.key.LEFT:
            self.player2.change_x = -MOVEMENT_SPEED2
        elif key == arcade.key.RIGHT:
            self.player2.change_x = MOVEMENT_SPEED2

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
        # Check if the player collides with a wall
        return arcade.check_for_collision_with_list(player, self.wall_list)
    
    def freeze_player2(self):
        # Disable player2 movement
        self.player2.change_x = 0
        self.player2.change_y = 0
        # Set the frozen flag to True
        self.player2_frozen = True
        # Schedule a method to unfreeze player2 after 7 seconds
        self.unfreeze_schedule = arcade.schedule(self.unfreeze_player2, 7)


    def unfreeze_player2(self, delta_time):
        # Enable player2 movement
        self.player2.change_x = MOVEMENT_SPEED2  # Adjust to the default movement speed
        self.player2.change_y = 0
        # Set the frozen flag to False
        self.player2_frozen = False
        # Cancel the schedule for unfreezing player2
        arcade.unschedule(self.unfreeze_schedule)

    def on_update(self, delta_time):
        
        # Move player 1
        self.player1.update() 
        if not self.player2_frozen:
            self.player2.update()
        if self.check_wall_collision(self.player1):
            self.player1.center_x -= self.player1.change_x
            self.player1.center_y -= self.player1.change_y
            
        if self.check_wall_collision(self.player2):
            self.player2.center_x -= self.player2.change_x
            self.player2.center_y -= self.player2.change_y
            
        # Move player 2

        self.physics_engine1.update()
        self.physics_engine2.update()
        
        # Check for collisions with coins
        coin_hit_list1 = arcade.check_for_collision_with_list(self.player1, self.coin_list)
        coin_hit_list2 = arcade.check_for_collision_with_list(self.player2, self.coin_list)

        for coin in coin_hit_list1:
            coin.remove_from_sprite_lists()
            self.score1 += 1

        for coin in coin_hit_list2:
            coin.remove_from_sprite_lists()
            self.score2 += 1
            
        # Check if all coins are collected
        if len(self.coin_list) == 0:
            if self.current_level < MAX_LEVEL:
                self.current_level += 1
                self.setup(self.current_level)
            else:
                self.game_over = True
                
        if self.powerup_list:
            freeze_hit_list = arcade.check_for_collision_with_list(self.player1, self.powerup_list)
            for powerup in freeze_hit_list:
                # Remove the power-up sprite from the list
                powerup.remove_from_sprite_lists()
                # Apply freeze effect to Player 2 only if not already frozen
                if not self.player2_frozen:
                    self.freeze_player2()
            
        if arcade.check_for_collision(self.player1, self.player2):
            self.game_over = True  
            
        # Check if players collide
        if arcade.check_for_collision(self.player1, self.player2):
            self.game_over = True  
            
        if self.player1.center_x < 0:
            self.player1.center_x = SCREEN_WIDTH
        elif self.player1.center_x > SCREEN_WIDTH:
            self.player1.center_x = 0

        if self.player2.center_x < 0:
            self.player2.center_x = SCREEN_WIDTH
        elif self.player2.center_x > SCREEN_WIDTH:
            self.player2.center_x = 0

        if self.game_over:
            arcade.close_window()


def main():
    game = PacmanGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.current_level = 1
    game.setup(game.current_level)
    arcade.run()

if __name__ == "__main__":
    main()
