from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.reward import Reward
from app.schemas.reward import RewardCreate, RewardUpdate


def create_reward(db: Session, reward: RewardCreate) -> Reward:
    db_reward = Reward(
        child_id=reward.child_id,
        name=reward.name,
        description=reward.description,
        points_cost=reward.points_cost,
        is_active=True,
        is_redeemed=False
    )
    db.add(db_reward)
    db.commit()
    db.refresh(db_reward)
    return db_reward


def get_reward(db: Session, reward_id: int) -> Optional[Reward]:
    return db.query(Reward).filter(Reward.id == reward_id).first()


def get_rewards(
        db: Session,
        child_id: int,
        skip: int = 0,
        limit: int = 100,
        is_active: Optional[bool] = None,
        is_redeemed: Optional[bool] = None
) -> List[Reward]:
    query = db.query(Reward).filter(Reward.child_id == child_id)

    if is_active is not None:
        query = query.filter(Reward.is_active == is_active)
    if is_redeemed is not None:
        query = query.filter(Reward.is_redeemed == is_redeemed)

    return query.offset(skip).limit(limit).all()


def update_reward(
        db: Session,
        reward_id: int,
        reward_data: RewardUpdate
) -> Optional[Reward]:
    db_reward = get_reward(db, reward_id)
    if not db_reward:
        return None

    update_data = reward_data.dict(exclude_unset=True)

    # Если награда отмечается как погашенная, добавляем дату погашения
    if "is_redeemed" in update_data and update_data["is_redeemed"]:
        update_data["redeemed_at"] = datetime.utcnow()

    for field, value in update_data.items():
        setattr(db_reward, field, value)

    db.commit()
    db.refresh(db_reward)
    return db_reward


def delete_reward(db: Session, reward_id: int) -> bool:
    db_reward = get_reward(db, reward_id)
    if not db_reward:
        return False

    db.delete(db_reward)
    db.commit()
    return True


def redeem_reward(
        db: Session,
        reward_id: int,
        child_id: int
) -> Optional[Reward]:
    """Погашение награды с проверкой баланса баллов"""
    db_reward = db.query(Reward).filter(
        and_(
            Reward.id == reward_id,
            Reward.child_id == child_id,
            Reward.is_active == True,
            Reward.is_redeemed == False
        )
    ).first()

    if not db_reward:
        return None

    # Получаем ребенка и проверяем баланс
    child = db_reward.child
    if child.points_balance < db_reward.points_cost:
        return None

    # Списываем баллы и отмечаем награду как погашенную
    child.points_balance -= db_reward.points_cost
    db_reward.is_redeemed = True
    db_reward.redeemed_at = datetime.utcnow()

    db.commit()
    db.refresh(db_reward)
    return db_reward