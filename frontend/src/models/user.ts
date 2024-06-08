export interface User {
  id: number;
  last_login: Date;
  username: string;
  date_joined: Date;
  is_active: boolean;
  role: string;
  max_device_nb: number;
  tournament?: string;
  team?: string;
}
