def point_in_rect(r_x1: int, r_y1: int, r_x2: int, r_y2: int, p_x: int, p_y: int):
    return (r_x1 <= p_x <= r_x2 and
            r_y1 <= p_y <= r_y2)



def centerize_rect_in_rect(w1: int, h1: int, x2: int, y2: int, w2: int, h2: int) -> (int, int):
    return x2 - (w1 - w2) // 2, y2 - (h1 - h2) // 2
