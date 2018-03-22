 /*
 *  Program for visualizing rotation data about the three IMU axes as calculated by the MPU6050 DMP
 *  and the complementary filter.
 */

//import processing.serial.*;

//Serial  myPort;
short   portIndex = 1; // Index of serial port in list (varies by computer)
int     lf = 10;       //ASCII linefeed
String  inString;      //String for testing serial communication

// x,y coordinates of circles 1, 2, 3 (pitch, roll, yaw)
int cx[] = {150, 450, 750};
int cy[] = {200, 200, 200};

// circle diameters
int d   = 200; 

// Data from dmp and complementary filters
float dmp[] = new float[3];
float cmp[] = new float[3];

Table table;
int totalRows = 0;
int curRow = 0;


/*
 * Draws a line of length len, centered at x, y at the specified angle
 */
void drawLine(int x, int y, int len, float angle) {
  pushMatrix();
  translate(x, y);
  rotate(angle);
  line(-len/2, 0, len/2, 0);
  popMatrix();
}

void settings()
{
  size(900, 400);
}


void setup() {
  //table = loadTable("angles_2018-03-16-194830.csv", "header");
  table = loadTable("angles_2018-03-16-194729.csv",  "header");
  
  totalRows = table.getRowCount();
  println(table.getRowCount() + " total rows in table"); 
  /*
  noLoop();
  for (TableRow row : table.rows()) {
    // NOTE: cannot have spaces between the columns after the ','..
    float rotationX = row.getFloat("rotation_x");
    float gyro_totalX = row.getFloat("gyro_total_x");
    float lastX = row.getFloat("last_x");
    
    float rotationY = row.getFloat("rotation_y");
    float gyro_totalY = row.getFloat("gyro_total_y");
    float lastY = row.getFloat("last_y");
    
    println(rotationX + ", " + gyro_totalX + ", " + rotationY + ", " + gyro_totalY);
    println("lastX: " + lastX + ", lastY: " + lastY);
  }
  loop();
  */
  frameRate(40);
}

void draw() {
  
  background(0);

  getReadings();
  
  // Draw the three background circles
  noStroke();
  fill(225);
  for (int i = 0; i < 3; i++) {
    ellipse(cx[i], cy[i], d, d);
  }
  
  // Draw the lines representing the angles
  for (int i = 0; i < 3; i++) {
    strokeWeight(3);
    stroke(255, 0, 0);
    drawLine(cx[i], cy[i], d, radians(cmp[i]));
    stroke(#2EBDF0);
    drawLine(cx[i], cy[i], d, radians(dmp[i]));
  }
  
  // Draw the explanatory text
  textSize(20);
  fill(255, 0, 0);
  text("Complementary Filter", 10, 20);
  
  fill(#2EBDF0);
  text("DMP", 10, 50);
  
  fill(255);
  text("Pitch", cx[0]-25, 75);
  text("Roll", cx[1]-22, 75);
  text("Yaw", cx[2]-22, 75);
  
  for (int i = 0; i < 3; i++) {
    fill(255, 0, 0);
    String str = String.format("%5.1f", cmp[i]);
    text(str, cx[i]-22, 350);
    fill(#2EBDF0);
    str = String.format("%5.1f", dmp[i]);
    text(str, cx[i]-22, 380);
  }
  
}



void getReadings() {
    if(curRow >= totalRows)
    {
      println("End of Data");
      noLoop();
    }
    else
    {
      TableRow row = table.getRow(curRow++);

      cmp[0] = row.getFloat("last_x");
      cmp[1] = row.getFloat("last_y");
      cmp[2] = 0.0;
    }
}


/*
 *  Read and process data from the serial port
 */
 /*
void serialEvent(Serial p) {
  inString = myPort.readString();
  
  try {
    // Parse the data
    //println(inString);
    String[] dataStrings = split(inString, ':');
    if (dataStrings.length == 4) {
      if (dataStrings[0].equals("CMP")) {
        for (int i = 0; i < dataStrings.length - 1; i++) {
          cmp[i] = float(dataStrings[i+1]);
        }
      } else if (dataStrings[0].equals("DMP")) {
        for (int i = 0; i < dataStrings.length - 1; i++) {
          dmp[i] = float(dataStrings[i+1]);
        }        
      } else {
        println(inString);
      }
    }
  } catch (Exception e) {
    println("Caught Exception");
  }
  
}
*/
