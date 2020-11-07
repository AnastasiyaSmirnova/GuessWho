export interface Response {
  status: string;
  text: string;
  url: string | null;
  names: string[] | null;
  correctName: string | null;

  id?: number;
}
