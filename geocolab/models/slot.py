from ..extensions import db
from datetime import datetime as dt, timedelta
from datetimerange import DateTimeRange
from collections import namedtuple

Gap = namedtuple('Gap', ['start', 'end', 'days'])


class Slot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    is_open = db.Column(db.Boolean)
    facility_id = db.Column(db.Integer, db.ForeignKey('facility.id'), nullable=False)

    @property
    def current_offer(self):
        # this is not the best, but it'll do for now
        today = dt.now().date()
        try:
            return next(m for m in self.offers if m.date_from <= today <= m.date_to)
        except StopIteration:
            return None

    def offers_in_range(self, date_from, date_to):
        date_range = DateTimeRange(date_from, date_to)
        offers = [o for o in self.offers if DateTimeRange(o.date_from, o.date_to).is_intersection(date_range)]
        return sorted(offers, key=lambda x: x.date_from)

    def gaps_in_range(self, date_from, date_to, min_length=None):
        offers = self.offers_in_range(date_from, date_to)
        oneday = timedelta(days=1)
        if len(offers) == 0:
            return [Gap(date_from, date_to, date_to - date_to)]
        else:
            gaps = []
            for i in range(len(offers)):
                o = offers[i]
                prev_o = gaps[-1][1] if gaps else (date_from - oneday)
                next_o = offers[i + 1].date_to if i == len(offers) - 1 else (date_to + oneday)
                if o.contains(prev_o) or o.follows(prev_o):
                    continue
                if o.contains(next_o) or o.precedes(next_o):
                    continue
                gaps.append(Gap(prev_o + oneday, next_o - oneday, (next_o - prev_o).days - 2))
            if min_length:
                gaps = [g for g in gaps if g.days >= min_length]
            return gaps



