def point_in_rect(r_x1: int, r_y1: int, r_x2: int, r_y2: int, p_x: int, p_y: int):
    return (r_x1 <= p_x <= r_x2 and
            r_y1 <= p_y <= r_y2)
