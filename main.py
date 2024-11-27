import chess
import time
from position_evaluator import PositionEvaluator
from chess_bot_controller import ChessBotController

def print_board(board):
    """Функция для вывода доски на экран в удобном формате."""
    ##print("\n" + board.unicode(borders=True) + "\n") старая версия
    board_str = board.unicode(borders=True)
    board_str = board_str.replace('|', '  | ')  #без этой хуйни шахзматы не читаемы, всё сплющено
    board_str = board_str.replace('---', '--------') #это абсолютно по конченому с точки зрения кода, но работает
    board_str = board_str.replace('a', '   a').replace('b', '   b').replace('c', '   c').replace('d', '   d ').replace('e', '  e').replace('f', '   f').replace('g', '   g').replace('h', '   h')
    print("\n" + board_str + "\n")

def get_user_move(board):
    """Функция для получения хода пользователя."""
    while True:
        user_input = input("Введите свой ход (например, e2e4): ").strip().lower()
        if len(user_input) == 4:
            try:
                from_square = chess.parse_square(user_input[:2])  # Например, 'e2'
                to_square = chess.parse_square(user_input[2:])    # Например, 'e4'
                move = chess.Move(from_square, to_square)
                
                # Проверяем, что ход допустим
                if move in board.legal_moves:
                    return move
                else:
                    print("Этот ход недопустим. Попробуйте снова.")
            except ValueError:
                print("Некорректный формат ввода. Попробуйте снова.")
        else:
            print("Неверный формат хода. Попробуйте снова.")

def main():
    # Создаем новую шахматную доску
    board = chess.Board()

    # Переменные для измерения времени
    total_bot_time = 0
    bot_moves_count = 0

    # Создаем контроллер для бота с возможностью настройки глубины поиска
    bot_controller = ChessBotController(dfs_depth=4, bfs_depth=3, ucs_depth=3)

    print("Добро пожаловать в шахматы! Белые ходят первыми.")
    
    # Играем до конца партии
    while not board.is_game_over():
        print_board(board)
        
        # Если ходят белые, запрашиваем ход
        if board.turn == chess.WHITE:
            print("Ваш ход:")
            user_move = get_user_move(board)
            board.push(user_move)
        else:
            # Ходит бот
            print("Ходит бот...")

            start_time = time.time()
            best_move = bot_controller.get_best_move(board)
            end_time = time.time()

            move_time = end_time - start_time #штука для замера времени. Применял в дебажинге
            total_bot_time += move_time
            bot_moves_count += 1
            average_time = total_bot_time / bot_moves_count

            print(f"Бот выбирает ход: {best_move}")
            print(f"Время, затраченное на ход: {move_time:.2f} секунд")
            print(f"Среднее время на ход: {average_time:.2f} секунд")

            board.push(best_move)

            position_evaluator = bot_controller.position_evaluator
            score = position_evaluator.evaluate(board) #показывает счёт для дебагинга
            print(f"Текущая оценка позиции для чёрных: {score}")
    
    # Игра завершена, выводим результат
    print_board(board)
    if board.is_checkmate():
        print("Мат! Игра завершена.")
    elif board.is_stalemate():
        print("Пат! Игра завершена.")
    elif board.is_insufficient_material():
        print("Недостаточно материала для мата. Игра завершена.")
    else:
        print("Игра завершена.")
    
if __name__ == "__main__":
    main()