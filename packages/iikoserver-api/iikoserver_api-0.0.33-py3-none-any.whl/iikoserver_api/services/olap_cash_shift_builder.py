from datetime import datetime

from iikoserver_api.schemas.cashshift import OlapCashShift


class OlapCashShiftBuilder:
    def __init__(self, items: list[dict]):
        self.items = items

    def process(self):
        result = []
        for item in self.items:
            id = f'{item.get('Document')}_{item.get('DateTime.Typed')}'
            result.append(
                OlapCashShift(
                    id=id,
                    session_number=item.get('Document'),
                    cash_shift_name=item.get('Session.CashRegister'),
                    close_date=datetime.fromisoformat(item.get('DateTime.Typed')),
                    amount=item.get('Sum.Incoming')
                )
            )

        return result
