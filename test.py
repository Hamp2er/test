import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist # Наш главный герой для движения

class FigureMover(Node):
    def __init__(self):
        # Создаем узел с именем 'cool_mover'
        super().__init__('cool_mover')
        
        # Создаем издателя в топик /turtle1/cmd_vel (для черепашки)
        # Если будешь запускать на реальном роботе, поменяй на '/cmd_vel'
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        
        # Таймер работает часто (10 раз в секунду), чтобы мы могли точно считать время
        self.timer = self.create_timer(0.1, self.timer_callback)
        
        # Наши переменные состояния (в "кармане" self)
        self.start_time = self.get_clock().now() # Засекаем время старта
        self.phase = "FORWARD" # Текущая фаза движения

    def timer_callback(self):
        msg = Twist()
        # Считаем, сколько секунд прошло с момента старта
        now = self.get_clock().now()
        elapsed = (now - self.start_time).nanoseconds / 1e9 # Перевод из наносекунд в секунды

        # ЛОГИКА: 2 секунды едем, потом 1 секунду поворачиваем
        if self.phase == "FORWARD":
            msg.linear.x = 2.0  # Скорость вперед
            msg.angular.z = 0.0 # Не поворачиваем
            if elapsed > 2.0:   # Если прошло больше 2 сек
                self.phase = "TURN"
                self.start_time = now # Сбрасываем таймер для новой фазы
        
        elif self.phase == "TURN":
            msg.linear.x = 0.0  # Стоим на месте
            msg.angular.z = 1.57 # Поворот (90 градусов в секунду)
            if elapsed > 1.0:   # Поворачиваем ровно 1 секунду
                self.phase = "FORWARD"
                self.start_time = now # Опять сбрасываем время

        # Отправляем команду
        self.publisher_.publish(msg)
        self.get_logger().info(f'Стадия: {self.phase}, время: {elapsed:.1f}')

def main():
    rclpy.init()
    node = FigureMover()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        # При остановке шлем пустой Twist, чтобы робот не уехал в бесконечность
        stop_msg = Twist()
        node.publisher_.publish(stop_msg)
        node.get_logger().info('Робот остановлен!')
    
    rclpy.shutdown()

if __name__ == '__main__':
    main()
    ###yapedr