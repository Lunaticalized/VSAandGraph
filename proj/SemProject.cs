
using System;
using System.IO;
using System.Collections.Generic;
using System.Linq;
using Microsoft.ProgramSynthesis.Transformation.Text;
using Microsoft.ProgramSynthesis.Transformation.Text.Semantics;
using Microsoft.ProgramSynthesis.Wrangling.Constraints;
using Microsoft.ProgramSynthesis.Transformation.Text.Description;
using Microsoft.ProgramSynthesis.Transformation.Text.Constraints;
using System.Collections;

namespace proj
{
    internal static class SemProject
    {

    	private static void Main(string[] args)
        {
            Hypo1();
            Hypo2();
            Hypo3();
        }


        private static void Hypo1()
        {
            string indir = @"C:\proj\hypo1\";
        	string outdir = @"C:\proj\hypo1\result\";
            int i = 0;
            
        	for(i = 0; i < 10000; i++){
        		try{
        			string filename = i.ToString();
            		Console.WriteLine(filename);
            		ConstructColor(indir, outdir, filename, i);
            		//IOModule(filename, i);	
            	}
            	catch(Exception e){
            		Console.WriteLine(i.ToString() + " skipped.");
            	}
        	}
            	
            
            
        }





        private static void Hypo2()
        {
            string[] ret = {"Address", "Author", "BillingCode", "City", "Email", "EmergencyCall", "FilePath", "Gender", "Log", "Name", "Phone", "ShippingCode"};
            string indir = @"C:\proj\hypo2\";
        	string outdir = @"C:\proj\hypo2\result\";
            int i = 0;
            foreach (string subtask in ret){
            	for(i = 0; i < 100; i++){
            		try{
            			string filename = subtask + i.ToString();
	            		Console.WriteLine(filename);
	            		ConstructColor(indir, outdir, filename, i);
	            		//IOModule(filename, i);	
	            	}
	            	catch(Exception e){
	            		Console.WriteLine(subtask + " skipped.");
	            	}
            	}
            	
            }
            
        }


        private static void Hypo3()
        {
            string indir = @"C:\proj\hypo3\";
        	string outdir = @"C:\proj\hypo3\result\";
            int i = 0;
            
        	for(i = 0; i < 1000; i++){
        		string filename = "testing" + i.ToString() + "_1_66";
        		try{
        			
            		Console.WriteLine(filename);
            		ConstructColor(indir, outdir, filename, i);
            		//IOModule(filename, i);	
            	}
            	catch(Exception e){
            		Console.WriteLine(filename + " skipped.");
            	}
        	}
        }



        private static void ConstructColor(string indir, string outdir, string filename, int index){
        	string path = indir + filename+".txt";
        	string[] readText = File.ReadAllLines(path);
        	int n = readText.Length;
        	int i, j, k;

        	Console.WriteLine(n.ToString()+" examples read.");
        	if (n > 100){
        		return;
        	}
        	HashSet<HashSet<int>> allPrograms = new HashSet<HashSet<int>>();
        	using (StreamWriter file = new StreamWriter(outdir+filename+"_newcolor.txt"))
	        {
	        	file.WriteLine(n);
	        	int total = n;
	        	int cnt = 0;
	            for(i = 0; i < n; i++){
	            	
            		cnt ++;
            		Console.WriteLine(filename + " " + cnt.ToString() + "/" + total.ToString());
                    try
                    {               
                        
                        string ex1 = readText[i];
                        
                        string[] debris1 = ex1.Split('^');
                        
                        if (debris1.Length == 2){
                            string[] input1 = debris1[0].Split('|');
                            
                            InputRow in1 = new InputRow(input1);
                            
                            string output1 = debris1[1];
                            
                            IEnumerable<Program> topKPrograms = LearnAllProgram(in1, output1);

                        	foreach (Program p in topKPrograms)
							{
							    if(p != null){
	                            	HashSet<int> prog = new HashSet<int>();
	                            	for(k = 0; k < n; k++){
	                            		string test = readText[k];
	                            		string[] debrisTest = test.Split('^');

	                            		string[] goin = debrisTest[0].Split('|');
	                            		InputRow go = new InputRow(goin);
	                            		string outs = debrisTest[1];
	                            		string ret = p.Run(go) as string;
	                            		if (ret == outs){
	                            			//Console.WriteLine(i.ToString() + " " + j.ToString() + " " + k.ToString());
	                            			prog.Add(k);
	                            		}
	                            	}
	                            	bool take = true;
	                            	allPrograms.RemoveWhere(s => s.IsSubsetOf(prog));
	                            	foreach (HashSet<int> pp in allPrograms){
	                            		if (prog.IsSubsetOf(pp)){
	                            			take = false;
	                            			break;
	                            		}
	                            	}
	                            	if (take)
	                    				allPrograms.Add(prog);
	          
	                            }
							}
                        }
                       
                        
                    }
                    catch (Exception e)
                    {
                        Console.WriteLine("Exception caught.");
                        Console.WriteLine(e);
                    }

	            }
	            int color = 0;
	            foreach (HashSet<int> prog in allPrograms){
		        	Console.WriteLine("=====");
		        	foreach (var v in prog){
		        		foreach (var u in prog){
		        			if (v < u){
		        				file.WriteLine(v.ToString() + " " + u.ToString() + " " + color.ToString());
		        				//Console.WriteLine(v.ToString() + " " + u.ToString() + " " + color.ToString());
		        			}
		        		}
		        	}
		        	color += 1;
		        }

	        }
        }



        private static void IOModule(string indir, string outdir, string filename, int index){
        	
        	string path = indir + filename+".txt";
        	string[] readText = File.ReadAllLines(path);
        	int n = readText.Length;
        	int i, j;

        	Console.WriteLine(n.ToString()+" examples read.");

        	if (n > 1000) return;

        	int total = n * (n - 1) / 2;
        	int cnt = 0;


        	using (StreamWriter file = new StreamWriter(outdir+filename+".txt"))
	        {
	        	file.WriteLine(n);
	            for(i = 0; i < n-1; i++){
	            	for(j = i + 1; j < n; j++){
                        try
                        {               
                            
                            string ex1 = readText[i];
                            string ex2 = readText[j];

                         
                            string[] debris1 = ex1.Split('^');
                            string[] debris2 = ex2.Split('^');

                            string res = "No";
                            string ret = i.ToString() + " " + j.ToString();
                            if (debris1.Length == 2 && debris2.Length == 2){
                                string[] input1 = debris1[0].Split('|');
                                string[] input2 = debris2[0].Split('|');
                                string output1 = debris1[1];
                                string output2 = debris2[1];

                                if (Check(input1, output1, input2, output2)){
                                    
                                    file.WriteLine(ret);
                                    res = "Yes";
                                }
                            }
                            cnt ++;

                            Console.WriteLine(ret + "-"+res+"("+cnt.ToString() + "/" + total.ToString() +")" + "-"+index.ToString()+"/1000");
                        }
                        catch (Exception e)
                        {
                            Console.WriteLine("Exception caught.");
                        }
	            		
	            	}
	            	
	            }
	        }

        }


        private static bool Check(string[] input1, string output1, string[] input2, string output2){
        	InputRow inputRow1 = new InputRow(input1);
        	InputRow inputRow2 = new InputRow(input2);

        	if (ExistProgram(inputRow1, output1, inputRow2, output2)){
        		return true;
        	}
        	else{
        		return false;
        	}
        }


        private static Program LearnProgram(InputRow inputRow1, string output1, InputRow inputRow2, string output2){
        	
        	var session = new Session();

        	IEnumerable<Constraint<IRow, object>> constraints = new[]
            {
                new Example(inputRow1, output1),
            	new Example(inputRow2, output2)
            };

            session.Constraints.Add(constraints);
            session.Constraints.Add(new ForbidTransformation(TransformationKind.IfThenElse));
            session.Constraints.Add(new ForbidTransformation(TransformationKind.Lookup));


            Program topRankedProgram = session.Learn();
            return topRankedProgram;
        }

        private static IEnumerable<Program> LearnAllProgram(InputRow inputRow1, string output1){
        	
        	var session = new Session();

        	IEnumerable<Constraint<IRow, object>> constraints = new[]
            {
                new Example(inputRow1, output1),
            	
            };

            session.Constraints.Add(constraints);
            session.Constraints.Add(new ForbidTransformation(TransformationKind.IfThenElse));
            session.Constraints.Add(new ForbidTransformation(TransformationKind.Lookup));


            IEnumerable<Program> topKPrograms = session.LearnTopK(30);
            return topKPrograms;
        }

        private static bool ExistProgram(InputRow inputRow1, string output1, InputRow inputRow2, string output2){
        	
        	var session = new Session();

        	IEnumerable<Constraint<IRow, object>> constraints = new[]
            {
                new Example(inputRow1, output1),
                new Example(inputRow2, output2)
            };

            session.Constraints.Add(constraints);
            session.Constraints.Add(new ForbidTransformation(TransformationKind.IfThenElse));
            session.Constraints.Add(new ForbidTransformation(TransformationKind.Lookup));


            Program topRankedProgram = session.Learn();
            return (topRankedProgram != null);
            //return topRankedProgram != null;
        }


        private static void LearnFormatName()
        {


        	var session = new Session();
            IEnumerable<Constraint<IRow, object>> constraints = new[]
            {

                new Example(new InputRow("Living"), "2016"),
                
                new Example(new InputRow("Living"), "2016"),
                //new Example(new InputRow("9-Jun-73"), "1973"),
            };
            session.Constraints.Add(constraints);
            // session.Constraints.Add(new ForbidTransformation(TransformationKind.IfThenElse));
            // session.Constraints.Add(new ForbidTransformation(TransformationKind.Lookup));

            Program topRankedProgram = session.Learn();
            
            if (topRankedProgram == null)
            {
                Console.Error.WriteLine("Error: failed to learn format name program.");
            }
            else
            {
                
               	string[] start = {"Living"};
               	int n = start.Length;
               	for(int i = 0; i < n; i++){
               		string formatted = topRankedProgram.Run(new InputRow(start[i])) as string;
                    Console.WriteLine("\"{0}\"", formatted);
               	}
                
            }
        }

    }
}
