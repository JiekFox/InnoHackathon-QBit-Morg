import React, { useState } from 'react';
import DropdownItem from './DropdownItem';
import LogoutModal from '../LogoutModal';
import icon from '../../assets/img/icon.png';
import { useAuth } from '../../utils/AuthContext'; // Подключаем AuthContext
import {
    MY_MEETUPS_OWNER,
    MY_MEETUPS_SUBSCRIBER,
    PROFILE
} from '../../constant/router';
import { useNavigate } from 'react-router-dom'; // Для навигации

export default function UserMenu({ userName }) {
    const [showLogoutModal, setShowLogoutModal] = useState(false);
    const { removeToken } = useAuth(); // Получаем метод для logout
    const navigate = useNavigate(); // Используем для переадресации

    const handleLogoutClick = () => {
        setShowLogoutModal(true); // Открываем модальное окно
    };

    const handleCloseModal = () => {
        setShowLogoutModal(false); // Закрываем модальное окно
    };

    const handleConfirmLogout = () => {
        removeToken(); // Удаляем токен через AuthContext
        navigate('/'); // Перенаправляем на главную страницу
    };

    return (
        <div className="user-info">
            <span className="user-name">{userName}</span>
            <img className="user-avatar" src={icon} alt="User Avatar" />
            <div className="user-dropdown">
                <DropdownItem
                    to={PROFILE}
                    title="Profile"
                    description="Explore your profile!"
                />
                <DropdownItem
                    to={MY_MEETUPS_SUBSCRIBER}
                    title="My Meetups (subscribed)"
                    description="View all the meetings you have subscribed to"
                />
                <DropdownItem
                    to={MY_MEETUPS_OWNER}
                    title="My Meetups (owned)"
                    description="View all the meetings you own"
                />
                <hr />
                <div
                    className="dropdown-item log-out"
                    onClick={handleLogoutClick}
                    role="button"
                >
                    Log Out
                </div>
            </div>
            {showLogoutModal && (
                <LogoutModal
                    onClose={handleCloseModal}
                    onConfirm={handleConfirmLogout} // Вызов функции logout
                />
            )}
        </div>
    );
}
