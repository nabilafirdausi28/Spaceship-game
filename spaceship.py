import pygame
import random
import math

# ==================== INISIALISASI ====================
# Inisialisasi semua modul pygame
pygame.init()
# Inisialisasi modul mixer untuk audio
pygame.mixer.init()

# Konfigurasi layar
SCREEN_WIDTH = 550  # Lebar layar dalam pixel
SCREEN_HEIGHT = 500  # Tinggi layar dalam pixel
FPS = 60  # Frame per second untuk smooth gameplay

# Membuat window game dengan ukuran yang sudah ditentukan
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
# Mengatur judul window
pygame.display.set_caption("Spaceship Game - Dodge the Enemies!")

# Icon
try:
    # Mencoba load icon untuk window game
    icon = pygame.image.load("logo.png")
    pygame.display.set_icon(icon)
except:
    # Jika file tidak ditemukan, skip saja (tidak fatal)
    pass

# ==================== AUDIO SETUP ====================
try:
    # Load background music dan set volume ke 30%
    background_music = pygame.mixer.Sound("background_music.wav.mp3")
    background_music.set_volume(0.3)
    
    # Load sound effect untuk scoring dan set volume ke 50%
    score_sound = pygame.mixer.Sound("score.wav.mp3")
    score_sound.set_volume(0.5)
    
    # Load sound effect untuk collision dan set volume ke 70%
    collision_sound = pygame.mixer.Sound("coliision.wav.mp3")
    collision_sound.set_volume(0.7)
except pygame.error as e:
    # Jika audio files tidak ditemukan, print warning tapi game tetap jalan
    print(f"Warning: File audio tidak ditemukan - {e}")
    print("Game akan berjalan tanpa suara")

# ==================== GAME FUNCTIONS ====================
def player(x, y):
    """
    Menggambar spaceship pemain di posisi (x, y)
    
    Args:
        x: Koordinat x pemain
        y: Koordinat y pemain
    """
    try:
        # Mencoba load dan draw image spaceship
        img_player = pygame.image.load("spaceship.png")
        screen.blit(img_player, (x, y))
    except:
        # Fallback: gambar kotak hijau jika image tidak ada
        pygame.draw.rect(screen, (0, 255, 0), (x, y, 40, 40))

def enemy(x, y):
    """
    Menggambar enemy di posisi (x, y)
    
    Args:
        x: Koordinat x enemy
        y: Koordinat y enemy
    """
    try:
        # Mencoba load dan draw image enemy
        img_enemy = pygame.image.load("enemy.png")
        screen.blit(img_enemy, (x, y))
    except:
        # Fallback: gambar lingkaran merah jika image tidak ada
        pygame.draw.circle(screen, (255, 0, 0), (int(x + 16), int(y + 16)), 16)

def collision(x_player, y_player, x_enemy, y_enemy):
    """
    Mengecek apakah terjadi collision antara player dan enemy
    menggunakan distance formula (Pythagorean theorem)
    
    Args:
        x_player: Koordinat x pemain
        y_player: Koordinat y pemain
        x_enemy: Koordinat x enemy
        y_enemy: Koordinat y enemy
    
    Returns:
        bool: True jika terjadi collision, False jika tidak
    """
    # Hitung jarak antara pusat player dan enemy
    distance = math.sqrt((x_player - x_enemy)**2 + (y_player - y_enemy)**2)
    # Return True jika jarak kurang dari 27 pixel (berarti collision)
    return distance < 27

def draw_text(text, font, color, surface, x, y):
    """
    Helper function untuk menggambar text di layar
    
    Args:
        text: String text yang akan digambar
        font: Font object pygame
        color: Tuple RGB untuk warna text
        surface: Surface pygame tempat text akan digambar
        x: Koordinat x text
        y: Koordinat y text
    """
    # Render text menjadi surface
    textobj = font.render(text, True, color)
    # Dapatkan rectangle dari text untuk positioning
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    # Gambar text ke surface
    surface.blit(textobj, textrect)

# ==================== FONTS ====================
# Membuat berbagai ukuran font untuk UI game
font_small = pygame.font.Font('freesansbold.ttf', 14)   # Untuk instruksi
font_medium = pygame.font.Font('freesansbold.ttf', 20)  # Untuk score dan level
font_large = pygame.font.Font('freesansbold.ttf', 32)   # Untuk text penting
font_title = pygame.font.Font('freesansbold.ttf', 48)   # Untuk title/game over

# ==================== GAME STATE ====================
def init_game():
    """
    Inisialisasi semua variabel game state ke nilai awal
    
    Returns:
        dict: Dictionary berisi semua game state variables
    """
    return {
        'score': 0,  # Score pemain saat ini
        'highscore': 0,  # Highscore tertinggi
        'x_player': SCREEN_WIDTH // 2,  # Posisi x pemain (tengah layar)
        'y_player': SCREEN_HEIGHT - 90,  # Posisi y pemain (bawah layar)
        'x_player_velocity': 0,  # Kecepatan horizontal pemain
        'x_enemy': random.randint(50, SCREEN_WIDTH - 80),  # Posisi x enemy random
        'y_enemy': random.randint(5, 10),  # Posisi y enemy mulai dari atas
        'y_enemy_velocity': 5.5,  # Kecepatan jatuh enemy
        'level': 1,  # Level saat ini
    }

def show_hud(game_state):
    """
    Menggambar HUD (Heads-Up Display) yang menampilkan score, level, dan instruksi
    
    Args:
        game_state: Dictionary berisi game state variables
    """
    # Gambar score di kiri atas
    draw_text(f"Score: {game_state['score']}", font_medium, (255, 255, 255), screen, 15, 15)
    
    # Gambar level di kanan atas
    draw_text(f"Level: {game_state['level']}", font_medium, (100, 200, 255), screen, SCREEN_WIDTH - 150, 15)
    
    # Gambar highscore di bawah level
    draw_text(f"High: {game_state['highscore']}", font_small, (255, 215, 0), screen, SCREEN_WIDTH - 150, 50)
    
    # Gambar instruksi kontrol di bawah layar
    draw_text("← → or A D to move | ESC to quit", font_small, (200, 200, 200), screen, 15, SCREEN_HEIGHT - 30)

def show_game_over_screen(game_state):
    """
    Menampilkan layar game over dengan final score dan highscore
    
    Args:
        game_state: Dictionary berisi game state variables
    """
    # Buat overlay semi-transparan hitam
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(200)  # Transparansi 200/255
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))
    
    # Gambar text "GAME OVER!" di tengah layar
    draw_text("GAME OVER!", font_title, (255, 0, 0), screen, SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT // 2 - 100)
    
    # Gambar final score
    draw_text(f"Final Score: {game_state['score']}", font_medium, (255, 255, 255), screen, SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2)
    
    # Gambar highscore dengan warna gold
    draw_text(f"Highscore: {game_state['highscore']}", font_medium, (255, 215, 0), screen, SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 50)
    
    # Gambar instruksi untuk restart atau quit
    draw_text("Press SPACE to restart or ESC to quit", font_small, (200, 200, 200), screen, SCREEN_WIDTH // 2 - 160, SCREEN_HEIGHT // 2 + 120)

# ==================== MAIN GAME LOOP ====================
# Membuat clock object untuk mengatur frame rate
clock = pygame.time.Clock()
running = True  # Flag untuk main loop
game_state = init_game()  # Inisialisasi game state
music_playing = False  # Flag untuk track apakah musik sudah diputar
game_over = False  # Flag untuk game over state

while running:
    # Fill background dengan warna biru gelap
    screen.fill((10, 10, 30))
    
    # Background stars effect - membuat efek bintang bergerak
    for i in range(20):
        # Hitung posisi x dengan scrolling effect
        x = (i * 30 + pygame.time.get_ticks() // 20) % SCREEN_WIDTH
        y = (i * 25) % SCREEN_HEIGHT
        # Gambar bintang sebagai circle kecil putih
        pygame.draw.circle(screen, (200, 200, 200), (x, y), 1)
    
    if not game_over:
        # ========== PLAYING STATE ==========
        
        # Mulai background music jika belum diputar
        if not music_playing:
            try:
                background_music.play(-1)  # -1 untuk loop infinite
                music_playing = True
            except:
                pass
        
        # Event handling - proses semua input dari user
        for event in pygame.event.get():
            # Event untuk close window
            if event.type == pygame.QUIT:
                running = False
            
            # Event untuk key press (tombol ditekan)
            if event.type == pygame.KEYDOWN:
                # Gerak ke kiri
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    game_state['x_player_velocity'] = -6
                # Gerak ke kanan
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    game_state['x_player_velocity'] = 6
                # Quit game
                if event.key == pygame.K_ESCAPE:
                    running = False
            
            # Event untuk key release (tombol dilepas)
            if event.type == pygame.KEYUP:
                # Stop movement saat tombol kiri dilepas
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    game_state['x_player_velocity'] = 0
                # Stop movement saat tombol kanan dilepas
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    game_state['x_player_velocity'] = 0
        
        # Update posisi player berdasarkan velocity
        game_state['x_player'] += game_state['x_player_velocity']
        
        # Boundary checking - jangan biarkan player keluar layar
        if game_state['x_player'] >= SCREEN_WIDTH - 40:
            game_state['x_player'] = SCREEN_WIDTH - 40  # Batas kanan
        if game_state['x_player'] <= 0:
            game_state['x_player'] = 0  # Batas kiri
        
        # Update posisi enemy - bergerak ke bawah
        game_state['y_enemy'] += game_state['y_enemy_velocity']
        
        # Enemy spawn logic - jika enemy sampai bawah layar
        if game_state['y_enemy'] >= SCREEN_HEIGHT:
            # Spawn enemy baru di posisi x random
            game_state['x_enemy'] = random.randint(0, SCREEN_WIDTH - 40)
            game_state['y_enemy'] = 0  # Reset ke atas layar
            game_state['score'] += 1  # Tambah score
            
            # Increase difficulty setiap 5 points
            if game_state['score'] % 5 == 0:
                game_state['level'] += 1  # Naikkan level
                game_state['y_enemy_velocity'] += 0.5  # Enemy jatuh lebih cepat
            
            # Play score sound effect
            try:
                score_sound.play()
            except:
                pass
        
        # Collision detection - cek apakah player kena enemy
        if collision(game_state['x_player'], game_state['y_player'], game_state['x_enemy'], game_state['y_enemy']):
            # Play collision sound effect
            try:
                collision_sound.play()
            except:
                pass
            
            # Update highscore jika score saat ini lebih tinggi
            if game_state['score'] > game_state['highscore']:
                game_state['highscore'] = game_state['score']
            
            # Set game over state
            game_over = True
            # Stop semua audio
            pygame.mixer.stop()
        
        # Draw game elements - gambar player, enemy, dan HUD
        player(game_state['x_player'], game_state['y_player'])
        enemy(game_state['x_enemy'], game_state['y_enemy'])
        show_hud(game_state)
    
    else:
        # ========== GAME OVER STATE ==========
        # Tampilkan layar game over
        show_game_over_screen(game_state)
        
        # Event handling untuk game over
        for event in pygame.event.get():
            # Event untuk close window
            if event.type == pygame.QUIT:
                running = False
            
            # Event untuk key press
            if event.type == pygame.KEYDOWN:
                # Restart game dengan SPACE
                if event.key == pygame.K_SPACE:
                    game_state = init_game()  # Reset game state
                    game_over = False  # Kembali ke playing state
                    music_playing = False  # Reset flag musik
                
                # Quit game dengan ESC
                if event.key == pygame.K_ESCAPE:
                    running = False
    
    # Update display - refresh layar dengan semua yang sudah digambar
    pygame.display.update()
    # Tick clock untuk maintain FPS
    clock.tick(FPS)

# ==================== CLEANUP ====================
# Stop semua audio
pygame.mixer.stop()
# Quit pygame dengan bersih
pygame.quit()
# Print final statistics
print(f"Final Score: {game_state['score']}")
print(f"Highscore: {game_state['highscore']}")