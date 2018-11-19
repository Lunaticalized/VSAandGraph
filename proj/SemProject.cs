
using System;
using System.IO;
using System.Collections.Generic;
using System.Linq;
using Microsoft.ProgramSynthesis.Transformation.Text;
using Microsoft.ProgramSynthesis.Transformation.Text.Semantics;
using Microsoft.ProgramSynthesis.Wrangling.Constraints;


namespace proj
{
    internal static class SemProject
    {

        private static void Main(string[] args)
        {
            //LearnFormatName();
            // Test();
            IOModule();
        }

        private static void IOModule(){
        	string path = @"C:\proj\prose-benchmarks-main\feed_sampled.txt";
        	string[] readText = File.ReadAllLines(path);
        	int n = readText.Length;
        	int i, j;

        	Console.WriteLine(n.ToString()+" examples read.");


        	int total = n * (n - 1) / 2;
        	int cnt = 0;


        	using (StreamWriter file = new StreamWriter(@"C:\proj\prose-benchmarks-main\graph_total_"+n.ToString()+".txt"))
	        {
	        	file.WriteLine(n);
	            for(i = 0; i < n-1; i++){
	            	for(j = i + 1; j < n; j++){
                        try
                        {               
                            
                            string ex1 = readText[i];
                            string ex2 = readText[j];

                            // Console.WriteLine(ex1);
                            // Console.WriteLine(ex2);
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

                            Console.WriteLine(ret + "-"+res+"("+cnt.ToString() + "/" + total.ToString() +")");
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


        private static bool ExistProgram(InputRow inputRow1, string output1, InputRow inputRow2, string output2){
        	// var session = new Session();

        	// IEnumerable<Constraint<IRow, object>> constraints = new[]
         //    {
         //        new Example(inputRow1, output1),
         //        new Example(inputRow2, output2)
         //    };

         //    session.Constraints.Add(constraints);

         //    Program topRankedProgram = session.Learn();
         //    return topRankedProgram != null;

        	IEnumerable<Constraint<IRow, object>> constraints = new[]
            {
                new Example(inputRow1, output1),
                new Example(inputRow2, output2)
            };

            Program topRankedProgram = Learner.Instance.Learn(constraints);
            return (topRankedProgram != null &&  !topRankedProgram.Serialize().Contains("symbol=\"ite\""));
            //return topRankedProgram != null;
        }


        private static void LearnFormatName()
        {


        	var session = new Session();
            IEnumerable<Constraint<IRow, object>> constraints = new[]
            {

                new Example(new InputRow("123 444 555"), "123-444-555"),
                new Example(new InputRow("(123) 456 789"), "123-456-789"),
                new Example(new InputRow("Xiating Ouyang"), "XO")
            };
            session.Constraints.Add(constraints);

            Program topRankedProgram = session.Learn();
            
            if (topRankedProgram == null)
            {
                Console.Error.WriteLine("Error: failed to learn format name program.");
            }
            else
            {
                // Run the program on some new inputs.
                string programSerialized = topRankedProgram.Serialize();
                if (programSerialized.Contains("symbol=\"ite\"")){
                	Console.WriteLine("hahaha");
                }
                Console.WriteLine(programSerialized);
               	string[] start = {"608 236 3405", "(987) 876 544"};
               	int n = start.Length;
               	for(int i = 0; i < n; i++){
               		string formatted = topRankedProgram.Run(new InputRow(start[i])) as string;
                    Console.WriteLine("\"{0}\"", formatted);
               	}
                
            }
        }

    }
}
