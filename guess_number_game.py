import random
import json
import os
from datetime import datetime

class GuessNumberGame:
    def __init__(self, min_range=1, max_range=100, max_attempts=10):
        """
        Инициализация игры
        
        Args:
            min_range (int): Минимальное число диапазона
            max_range (int): Максимальное число диапазона
            max_attempts (int): Максимальное количество попыток
        """
        self.min_range = min_range
        self.max_range = max_range
        self.max_attempts = max_attempts
        self.secret_number = None
        self.attempts = 0
        self.guesses = []
        self.stats_file = "game_stats.json"
        self.start_time = None
        
    def generate_secret_number(self):
        """Генерация случайного числа"""
        self.secret_number = random.randint(self.min_range, self.max_range)
        self.attempts = 0
        self.guesses = []
        self.start_time = datetime.now()
        
    def display_welcome(self):
        """Отображение приветственного сообщения"""
        print("🎯 Добро пожаловать в игру 'Угадай число'!")
        print("=" * 50)
        print(f"Я загадал число от {self.min_range} до {self.max_range}.")
        print(f"У вас есть {self.max_attempts} попыток, чтобы угадать его!")
        print("После каждой попытки я подскажу, больше или меньше ваше число.")
        print("=" * 50)
        
    def get_user_guess(self):
        """Получение и валидация ввода пользователя"""
        while True:
            try:
                guess = input(f"\nПопытка {self.attempts + 1}/{self.max_attempts}. Ваше предположение: ")
                
                # Проверка на пустой ввод
                if not guess.strip():
                    print("❌ Ошибка: Введите число!")
                    continue
                    
                guess = int(guess)
                
                # Проверка диапазона
                if guess < self.min_range or guess > self.max_range:
                    print(f"❌ Число должно быть в диапазоне от {self.min_range} до {self.max_range}!")
                    continue
                    
                return guess
                
            except ValueError:
                print("❌ Ошибка: Пожалуйста, введите целое число!")
                
    def check_guess(self, guess):
        """Проверка предположения пользователя"""
        self.attempts += 1
        self.guesses.append(guess)
        
        if guess == self.secret_number:
            return "win"
        elif guess < self.secret_number:
            return "too_low"
        else:
            return "too_high"
            
    def provide_hint(self, result, guess):
        """Предоставление подсказки пользователю"""
        if result == "too_low":
            print(f"📈 Загаданное число БОЛЬШЕ чем {guess}")
        elif result == "too_high":
            print(f"📉 Загаданное число МЕНЬШЕ чем {guess}")
            
        # Дополнительная подсказка после нескольких попыток
        if self.attempts == 3:
            range_hint = self.get_range_hint()
            print(f"💡 Подсказка: число находится между {range_hint[0]} и {range_hint[1]}")
            
    def get_range_hint(self):
        """Генерация подсказки о диапазоне"""
        lower_bound = max(self.min_range, self.secret_number - 20)
        upper_bound = min(self.max_range, self.secret_number + 20)
        return (lower_bound, upper_bound)
        
    def display_attempts_left(self):
        """Отображение оставшихся попыток"""
        attempts_left = self.max_attempts - self.attempts
        if attempts_left <= 3:
            print(f"⚠️  Осталось попыток: {attempts_left}")
            
    def save_game_stats(self, won):
        """Сохранение статистики игры"""
        end_time = datetime.now()
        duration = (end_time - self.start_time).seconds
        
        stats = {
            'timestamp': datetime.now().isoformat(),
            'secret_number': self.secret_number,
            'attempts': self.attempts,
            'won': won,
            'duration_seconds': duration,
            'guesses': self.guesses,
            'range': f"{self.min_range}-{self.max_range}"
        }
        
        # Загрузка существующей статистики
        all_stats = self.load_all_stats()
        all_stats.append(stats)
        
        # Сохранение обновленной статистики
        try:
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(all_stats, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️  Не удалось сохранить статистику: {e}")
            
    def load_all_stats(self):
        """Загрузка всей статистики"""
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return []
        return []
        
    def display_stats(self):
        """Отображение общей статистики"""
        stats = self.load_all_stats()
        if stats:
            total_games = len(stats)
            wins = sum(1 for game in stats if game['won'])
            win_rate = (wins / total_games) * 100
            
            print(f"\n📊 Статистика игр:")
            print(f"   Всего игр: {total_games}")
            print(f"   Побед: {wins} ({win_rate:.1f}%)")
            
    def play_round(self):
        """Игровой раунд"""
        self.generate_secret_number()
        self.display_welcome()
        
        while self.attempts < self.max_attempts:
            guess = self.get_user_guess()
            result = self.check_guess(guess)
            
            if result == "win":
                print(f"\n🎉 Поздравляем! Вы угадали число {self.secret_number}!")
                print(f"🏆 Количество попыток: {self.attempts}")
                self.save_game_stats(True)
                return True
            else:
                self.provide_hint(result, guess)
                self.display_attempts_left()
                
        print(f"\n💔 К сожалению, вы исчерпали все {self.max_attempts} попыток.")
        print(f"🔢 Загаданное число было: {self.secret_number}")
        self.save_game_stats(False)
        return False
        
    def ask_for_replay(self):
        """Запрос на повторную игру"""
        while True:
            choice = input("\n🔄 Хотите сыграть еще раз? (да/нет): ").lower().strip()
            if choice in ['да', 'д', 'yes', 'y']:
                return True
            elif choice in ['нет', 'н', 'no', 'n']:
                return False
            else:
                print("❌ Пожалуйста, введите 'да' или 'нет'")

def main():
    """Основная функция программы"""
    game = GuessNumberGame(min_range=1, max_range=100, max_attempts=10)
    
    print("=" * 60)
    print("           ИГРА 'УГАДАЙ ЧИСЛО'")
    print("=" * 60)
    
    while True:
        game.play_round()
        game.display_stats()
        
        if not game.ask_for_replay():
            print("\n👋 Спасибо за игру! До свидания!")
            break
            
        print("\n" + "=" * 50)
        print("          НОВАЯ ИГРА")
        print("=" * 50)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Игра прервана. До свидания!")
    except Exception as e:
        print(f"\n❌ Произошла непредвиденная ошибка: {e}")
