// App.tsx
import React, { useState, useEffect } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import AuthNavigator from './src/navigation/AuthNavigator';
import MainNavigator from './src/navigation/MainNavigator';
import FloatingButton from './src/components/FloatingButton';
import Overlay from './src/components/Overlay';
import EncryptedStorage from 'react-native-encrypted-storage';
import SplashScreen from './src/screens/Auth/SplashScreen';


const App = (): JSX.Element => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [isOverlayVisible, setOverlayVisible] = useState(false);
  const [userType, setUserType] = useState<string | null>(null); // User type: 'family' or 'socialWorker'

  useEffect(() => {
    const fetchUserType = async () => {
      // const storedUserType = await EncryptedStorage.getItem('userType');
      // setUserType(storedUserType);
      setUserType('family');
    };
    if (isLoggedIn) {
      fetchUserType();
    }
  }, [isLoggedIn]);

  const toggleOverlay = () => {
    setOverlayVisible(!isOverlayVisible);
  };

  return (
    <NavigationContainer>
      {isLoggedIn ? (
        <>
          <MainNavigator userType={userType} setIsLoggedIn={setIsLoggedIn}/>
          {/* 오버레이 */}
          {isOverlayVisible && <Overlay onClose={toggleOverlay} />}
          {/* 플로팅 버튼 */}
          <FloatingButton toggleOverlay={toggleOverlay} />
        </>
      ) : (
        <AuthNavigator setIsLoggedIn={setIsLoggedIn} />
      )}
    </NavigationContainer>
  );
};

export default App;
