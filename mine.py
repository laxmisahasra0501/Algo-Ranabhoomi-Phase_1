from adapter import Solver, cost_of
import time

class MySolver(Solver):

    def solve(self, instance, submit_candidate):
        order = sorted(
            range(instance.size),
            key=lambda b: (instance.due[b], b)
        )

        receipt = submit_candidate({"order": order})
        end_time = time.monotonic() + receipt["remaining_s"] - 0.3
        best_cost = cost_of(instance, order)

        while time.monotonic() < end_time:
            improved = False

            for i in range(len(order)):
                if time.monotonic() >= end_time:
                    break

                batch = order.pop(i)
                best_pos = i

                for j in range(len(order) + 1):
                    if time.monotonic() >= end_time:
                        break

                    order.insert(j, batch)
                    c = cost_of(instance, order)

                    if c < best_cost:
                        best_cost = c
                        best_pos = j
                        improved = True

                    order.pop(j)

                order.insert(best_pos, batch)

            if not improved:
                break

        submit_candidate({"order": order})
        return {"order": order}
