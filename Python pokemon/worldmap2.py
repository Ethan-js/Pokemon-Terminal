import curses
import time
from deco import *
from map_saver import *
worldmap2 = r"""
                                                  __________________                        \"""/                                                     \"""/ 
\"""/       \"""/                                /                  \                                                                                                           \"""/
                              \|/               /         |          \                                                                                                                                                   \|/
                                               /        --+--         \                                                                                           \|/
     \"""/                                    /___________|____________\                                                                                                         \|/   
                                              |                        |                                                                                                                        \|/
                                              |                        |                                             \|/                                              \|/
                                              |         ______         |                                                                                                        
                   \"""/                      |        |      |        |                                                        \|/                                                                                   \|/
                                              |        |      |        |                                                                     \|/                                    
                                              |        |      |        |                                                                                                                        \"""/
                                              |________|      |________|                                                                         \"""/                            
       \""/                         \|/               |        |                                                                                                                                                                                        \|/
                                                      |        |                                                    \|/                                              \|/                                                                                                                                                                  
                                                      |        |         \***/\***/\***/\***/\***/\***/\***/\***/\***/                                                                                                  \""/ 
                                                      |        |         \***/\***/\***/\***/\***/\***/\***/\***/\***/                    \"""/                                                       \|/
                            \|/                       |        |         \***/\***/\***/\***/\***/\***/\***/\***/\***/                                                                                                                      \"""/
                                                      |        |         \***/\***/\***/\***/\***/\***/\***/\***/\***/                                                        \|/
 \"""/                                                |        |         \***/\***/\***/\***/\***/\***/\***/\***/\***/                                  \"""/
                                       \""/           |        |         \***/\***/\***/\***/\***/\***/\***/\***/\***/                                                                       \""/ 
                                                      |        |         \***/\***/\***/\***/\***/\***/\***/\***/\***/                                                                                           \|/
                                                      |        |         \***/\***/\***/\***/\***/\***/\***/\***/\***/                                                                                                          \|/
                 \""/                                 |        |                                              \|/                                              \|/                                              \|/
                                                      |        |____________________________________                                                                                                                \"""/
                                                      |                                             |                                                                   \"""/
       \|/                              \|/           |                                             | 
                                                      |                                             |                             \"""/
                                                      |____________________________________         |                                          \"""/
                                                                                           |        |                                                                                                           \"""/
                                                                                           |        |                \|/                                                                                \|/                                                                    
                                                          \***/\***/\***/\***/\***/\***/   |        |                                                                                                \"""/              
                                                          \***/\***/\***/\***/\***/\***/   |        |                                                               \|/                                              \|/                                                                     
                                                          \***/\***/\***/\***/\***/\***/   |        |                                                                                                                       \|/
                             _             _              \***/\***/\***/\***/\***/\***/   |        |                                                                                             \|/
                            / \           / \             \***/\***/\***/\***/\***/\***/   |        |                          \|/                                     \"""/
                           |   |         |   |            \***/\***/\***/\***/\***/\***/   |        |                                                         \""/ 
                          /     \       /     \           \***/\***/\***/\***/\***/\***/   |        |                                                                                                   \"""/
                         |       |     |       |                                           |        |                                        
                        /         \   /         \                                          |        |                                                               \|/                      \"""/                        \|/
                       |___________| |___________|                                         |        | 
                           |   |         |   |                                             |        |                                                   \|/
                           |   |         |   |                                             |        |                                                                                                                                           \"""/
                           |   |         |   |                                             |        |                                               \|/
                                                                                           |        | 
                                                                                           |        | 
                                                                                           |        | 

















"""
worldmap2 = worldmap3


playersprite = r""" '''''
(  o o)
    ⌣
  /|\
  / \ """[:-1]

playersprite1 = r""" '''''
(  o o)
    ⌣
  /|\
   | """
playersprite2 = r""" '''''
(o o  )
  ⌣
  /|\
  / \ """[:-1]
playersprite3 = r""" '''''
(o o  )
  ⌣
  /|\
   | """

playersprite4 = r""" '''''
(     )
 
  /|\
  /  """

playersprite5 = r""" '''''
(     )
    
  /|\
    \ """[:-1]
playersprite6 = r""" '''''
( o o )
   ⌣
  /|\
  /  """
playersprite7 = r""" '''''
( o o )
   ⌣
  /|\
    \ """[:-1]