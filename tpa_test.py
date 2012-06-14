#!/usr/bin/env python


def TPAtoATPA(TPA, dist):
    Result = []
    c = 0
    l = len(TPA)
    for a in range(0, l):
        found = False
        for b in range(0, c-1):
            if round(((TPA[a][0] - Result[b][0][0])**2 + (TPA[a][1] - Result[b][0][1])**2)**0.5) <= dist:
                found = True
                break
        if found:
            Result[b].append(TPA[a])
        else:
            Result.append([TPA[a]])
            c += 1
    return Result

def getTPABounds(TPA):
    L = len(TPA)
    if L < 0:
        return -1
   
    seed_blob = TPA[0]
    left, right, top, bottom = seed_blob[0], seed_blob[0], seed_blob[1], seed_blob[1]
    
    for i in range(1, L):
        if TPA[i][0] < left:
            left = TPA[i][0]
        elif TPA[i][0] > right:
            right = TPA[i][0]
        if TPA[i][1] < top:
            top = TPA[i][1]
        elif TPA[i][1] > bottom:
            bottom = TPA[i][1]

    return ((left, top), (right, bottom))


"""
function GetTPABounds(const TPA: TPointArray): TBox;
var
  I,L : Integer;
begin;
  FillChar(result,sizeof(TBox),0);
  L := High(TPA);
  if (l < 0) then Exit;
  Result.x1 := TPA[0].x;
  Result.y1 := TPA[0].y;
  Result.x2 := TPA[0].x;
  Result.y2 := TPA[0].y;
  for I:= 1 to L do
  begin;
    if TPA[i].x > Result.x2 then
      Result.x2 := TPA[i].x
    else if TPA[i].x < Result.x1 then
      Result.x1 := TPA[i].x;
    if TPA[i].y > Result.y2 then
      Result.y2 := TPA[i].y
    else if TPA[i].y < Result.y1 then
      Result.y1 := TPA[i].y;
  end;
end;
"""



"""
function TPAtoATPA(const TPA: TPointArray; Dist: Integer): T2DPointArray;
var
   a, b, c, l: LongInt;
   Found: Boolean;
begin
  SetLength(Result, 0);
  l := High(tpa);
  c := 0;
  for a := 0 to l do
  begin
    Found := false;
    for b := 0 to c -1 do
      if (Round(sqrt(Sqr(TPA[a].X - Result[b][0].X) + Sqr(TPA[a].Y - Result[b][0].Y))) <= Dist) then
      begin
        Found := True;
        Break;
      end;
    if Found then
//    if (b < c) then
    begin
      SetLength(Result[b], Length(Result[b]) + 1);
      Result[b][High(Result[b])] := TPA[a];
    end else
    begin
      SetLength(Result, c + 1);
      SetLength(Result[c], 1);
      Result[c][0] := TPA[a];
      Inc(c);
    end;
  end;
end;
"""

if __name__ == "__main__":

    tpa = [[428, 241], [325, 336], [344, 339], [388, 79], [391, 252], [340, 294], [420, 283], [356, 264], [375, 334], [381, 149], [356, 35], [455, 89]]

    atpa = TPAtoATPA(tpa, 100)

    print atpa

    for x in atpa:
        print x
        print getTPABounds(x)






