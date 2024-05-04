export interface UserPatch extends Partial<User> {
  current_password?: string;
  new_password?: string;
  password_validation?: string;
}

export interface User {
  id: number;
  last_login: Date;
  username: string;
  date_joined: Date;
  is_staff: boolean;
  is_superuser: boolean;
  is_active: boolean;
  groups: string[];
  user_permissions: unknown[];
}

export interface UserPatchError {
  user?: string[];
  password?: string;
}
