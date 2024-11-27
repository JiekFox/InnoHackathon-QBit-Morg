import React, { createContext, useState, useContext, useEffect } from 'react';

const AuthContext = createContext();

export const useAuth = () => {
    return useContext(AuthContext);
};

export const AuthProvider = ({ children }) => {
    const [token, setToken] = useState(null);
    const [name, setName] = useState(null);
    const [userID, setUserID] = useState(null);
    const [loading, setLoading] = useState(true);

    const saveToken = newToken => {
        setToken(newToken);
        localStorage.setItem('authToken', JSON.stringify(newToken));
    };
    const saveName = newName => {
        setName(newName);
        localStorage.setItem('name', JSON.stringify(newName));
    };
    const saveId = newID => {
        setUserID(newID);
        localStorage.setItem('ID', JSON.stringify(newID));
    };
    const saveDate = newDate => {
        console.log(newDate);
        saveToken({
            refresh: newDate.refresh,
            access: newDate.access
        });
        saveName(newDate.username);
        saveId(newDate.user_id);
        setLoading(false);
    };

    const removeToken = () => {
        setToken(null);
        setUserID(null);
        setName(null);
        localStorage.removeItem('authToken');
        localStorage.removeItem('name');
        localStorage.removeItem('ID');
    };

    useEffect(() => {
        const savedToken = localStorage.getItem('authToken');
        if (savedToken) {
            try {
                const parsedToken = JSON.parse(savedToken);
                setToken(parsedToken);
                //console.log("Token loaded from localStorage:", parsedToken);
            } catch (error) {
                console.error('Failed to parse token from localStorage:', error);
            }
        }
        const savedName = localStorage.getItem('name');
        if (savedName) {
            try {
                const parsedName = JSON.parse(savedName); // Парсим токен
                setName(parsedName);
                //console.log("Token loaded from localStorage:", parsedToken);
            } catch (error) {
                console.error('Failed to parse name from localStorage:', error);
            }
        }
        const savedID = localStorage.getItem('ID');
        if (savedID) {
            try {
                const parsedID = JSON.parse(savedID);
                setUserID(parsedID);
                //console.log("Token loaded from localStorage:", parsedToken);
            } catch (error) {
                console.error('Failed to parse ID from localStorage:', error);
            }
        }
        setLoading(false);
    }, []);
    console.log(name, userID, token);
    /*
  useEffect(() => {
    if (token && token.access) {
      try {
        const extractedUserID = getUserIdFromToken(token.access);
        setUserID(extractedUserID);
        console.log("User ID from token:", extractedUserID);
      } catch (error) {
        console.error("Error extracting user ID from token:", error);
      }
    } else {
      console.log("No valid token available.");
    }
  }, [token]);*/
    /*

  useEffect(() => {
    if (userID) {
      const { data: meetup, loading, error } = useFetchMeetings(
          `${MEETINGS_API_URL}${userID}/`
      );

      if (loading) {
        console.log("Loading user data...");
      }

      if (error) {
        console.error("Error fetching user data:", error);
      }

      if (meetup && meetup.name) {
        setName(meetup.name); // Сохраняем имя пользователя
        console.log("User name fetched:", meetup.name);
      }
    }
  }, [userID]);*/

    const value = {
        token,
        userID,
        name,
        saveToken,
        removeToken,
        saveDate,
        loading
    };

    return loading ? (
        <div>Loading...</div>
    ) : (
        <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
    );
};
