package com.mytest;

import java.io.*;


public class MyTest {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		System.out.println("Hello");
		
		MyTest myVar = new MyTest();
//		myVar.encode("cacert.pem", "out.hex");
		myVar.decode("dctstudy.txt", "dctstudy.bin");		
		
		System.out.println("End");
	}
	
	@SuppressWarnings("unused")
	private void decode(String ifile, String ofile)
	{
		ReadWriteBinaryFile rwFile = new ReadWriteBinaryFile(ifile, ofile);
		byte[] rawarr = rwFile.readFile();
		String str = new String(rawarr);
		
		try
		{
			byte[] byteArr = {0};
			BufferedReader reader = new BufferedReader(new StringReader(str));
			String line = reader.readLine();
			try {
				while (line != null)
				{
					byteArr = HexEncode.hex2bin(line);
					rwFile.writeFile(byteArr, false);
					line = reader.readLine();
				}
				rwFile.writeFile(byteArr, true);
			}
			catch (NumberFormatException e){
				System.out.println("Error: " + e.getMessage());
			}
		}
		catch(IOException exc)
		{
			System.out.println("Error: " + exc.getMessage());
		}

		System.out.print(str);
	}
	
	@SuppressWarnings("unused")
	private void encode(String ifile, String ofile)
	{
		ReadWriteBinaryFile rwFile = new ReadWriteBinaryFile(ifile, ofile);
		byte[] rawarr = rwFile.readFile();
		
		// split into 16 bytes rows and feed to hex encoder
		byte[] arrRows = new byte[16];
		String encStr;
		
		System.out.println("filelength " + rawarr.length);
		
		int looprem = rawarr.length % 16;
		int loopcnt = rawarr.length / 16;
		if (looprem > 0) loopcnt++;
		int bytesRead = 0;
		
		for(int i=0; i<loopcnt; i++)
		{
			if ((bytesRead + looprem) == rawarr.length) // last row
			{
				byte[] lastrow = new byte[looprem];
				System.arraycopy(rawarr, i*16, lastrow, 0, looprem);
				encStr = HexEncode.getHex(lastrow);
				rwFile.writeFile(encStr, true); // close file
				bytesRead += looprem;
			}
			else
			{
				System.arraycopy(rawarr, i*16, arrRows, 0, 16);
				encStr = HexEncode.getHex(arrRows);
				rwFile.writeFile(encStr, false);
				bytesRead += 16;
			}
			
			System.out.println(encStr);
		}
	}
}


class HexEncode
{
	private static final String    HEXES    = "0123456789ABCDEF";

	public static String getHex(byte[] raw) {
	    final StringBuilder hex = new StringBuilder(2 * raw.length);
	    for (final byte b : raw) {
	        hex.append(HEXES.charAt((b & 0xF0) >> 4)).append(HEXES.charAt((b & 0x0F)));
	    }
	    return hex.toString();
	}
	
	public static char[] encodeHex( final byte[] data ){
	    final int l = data.length;
	    final char[] out = new char[l<<1];
	    for( int i=0,j=0; i<l; i++ ){
	        out[j++] = HEXES.charAt((0xF0 & data[i]) >>> 4);
	        out[j++] = HEXES.charAt(0x0F & data[i]);
	    }
	    return out;
	}
	
	/**
	 * Decodes a hexadecimally encoded binary string.
	 * <p>
	 * Note that this function does <em>NOT</em> convert a hexadecimal number to a
	 * binary number.
	 *
	 * @param hex Hexadecimal representation of data.
	 * @return The byte[] representation of the given data.
	 * @throws NumberFormatException If the hexadecimal input string is of odd
	 * length or invalid hexadecimal string.
	 */
	public static byte[] hex2bin(String hex) throws NumberFormatException {
		if (hex.length() % 2 > 0) {
			throw new NumberFormatException("Hexadecimal input string must have an even length.");
		}
		byte[] r = new byte[hex.length() / 2];
		for (int i = hex.length(); i > 0;) {
			r[i / 2 - 1] = (byte) (digit(hex.charAt(--i)) | (digit(hex.charAt(--i)) << 4));
		}
		return r;
	}

	private static int digit(char ch) {
		int r = Character.digit(ch, 16);
		if (r < 0) {
			throw new NumberFormatException("Invalid hexadecimal string: " + ch);
		}
		return r;
	}
}



class ReadWriteBinaryFile
{
	private String inFilename;
	private String outFilename;
	private BufferedWriter outFileHandle;
	private OutputStream output;

	public ReadWriteBinaryFile(String inFile, String outFile) 
	{
		inFilename = inFile;
		outFilename = outFile;
		outFileHandle = null;
		output = null;
	}
	
	public byte[] readFile() 
	{
		//System.out.println("Reading binary file into byte array example");
		try{
			//Instantiate the file object
			File file = new File(inFilename);
			//Instantiate the input stream
			InputStream insputStream = new FileInputStream(file);
			long length = file.length();
			byte[] bytes = new byte[(int) length];

			insputStream.read(bytes);
			insputStream.close();
			
			return bytes;

//			String s = new String(bytes);
			//Print the byte data into string format
//			System.out.println(s);
		}catch(Exception e){
			System.out.println("Error is:" + e.getMessage());
		}
		
		return null;
	}
	
	public int writeFile(String inStr, boolean end)
	{
		try{
			//Instantiate the file object
			if (outFileHandle == null)
			{
				outFileHandle = new BufferedWriter(new FileWriter(outFilename, false));
			}

			outFileHandle.write(inStr);
			outFileHandle.newLine();
			outFileHandle.flush();
			
			return inStr.length();
			//return inStr.getBytes().length;

		}catch(Exception e){
			System.out.println("Error is:" + e.getMessage());
		} finally { // always close the file
			if (end == true)
			{
				try {
					outFileHandle.close();
					outFileHandle = null;
				} catch (IOException ioe2) {
					// just ignore it
				}
			}
		} 
		
		return 0;
	}
	
	/**
	   Write a byte array to the given file. 
	   Writing binary data is significantly simpler than reading it. 
	 */
	public int writeFile(byte[] aInput, boolean end)
	{
		int res;
		
		System.out.println("Writing binary file...");
		try {			
			//Instantiate the file object
			if (output == null)
			{
				output = new BufferedOutputStream(new FileOutputStream(outFilename));
			}

			try {
				if (end == false)
				{
					output.write(aInput);
				}
			}
			finally {
				if (end == true)
				{
					try {
						output.close();
						output = null;
					} catch (IOException ioe2) {
						// just ignore it
					}
				}
			}
		}
		catch(FileNotFoundException ex){
			System.out.println("File not found.");
		}
		catch(IOException ex){
			System.out.println(ex);
		}
		
		return 0;
	}

}



/*
https://stackoverflow.com/questions/36250571/filewriter-vs-fileoutputstream-in-java
-----------------------------------------------------------------------------------
FileWriter is a Writer. It's about writing text - and it happens to be writing it to a file. It does that 
by holding a reference to a FileOutputStream, which is created in the FileWriter constructor and passed 
to the superclass constructor.

FileOutputStream is an OutputStream. It's about writing binary data. If you want to write text to it, you 
need something to convert that text to binary data - and that's exactly what FileWriter does. Personally
I prefer to use FileOutputStream wrapped in an OutputStreamWriter by me to allow me to specify the character 
encoding (as FileWriter always uses the platform default encoding, annoyingly).

Basically, think of FileWriter as a simple way of letting you write:

Writer writer = new FileWriter("test.txt");

instead of

Writer writer = new OutputStreamWriter(new FileOutputStream("test.txt"));

Except I'd normally recommend using the overload of the OutputStreamWriter constructor that accepts a Charset.
*/


