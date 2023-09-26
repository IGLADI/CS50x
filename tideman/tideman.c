#include <cs50.h>
#include <string.h>
#include <stdio.h>

// Max number of candidates
#define MAX 9

// preferences[i][j] is number of voters who prefer i over j
int preferences[MAX][MAX];

// locked[i][j] means i is locked in over j
bool locked[MAX][MAX];

// Each pair has a winner, loser
typedef struct
{
    int winner;
    int loser;
}
pair;

// Array of candidates
string candidates[MAX];
pair pairs[MAX * (MAX - 1) / 2];

int pair_count;
int candidate_count;

// Function prototypes
bool vote(int rank, string name, int ranks[]);
void record_preferences(int ranks[]);
void add_pairs(void);
void sort_pairs(void);
void lock_pairs(void);
void print_winner(void);
bool circle(int a, int b);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: tideman [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i] = argv[i + 1];
    }

    // Clear graph of locked in pairs
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            locked[i][j] = false;
        }
    }

    pair_count = 0;
    int voter_count = get_int("Number of voters: ");

    // Query for votes
    for (int i = 0; i < voter_count; i++)
    {
        // ranks[i] is voter's ith preference
        int ranks[candidate_count];

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            if (!vote(j, name, ranks))
            {
                printf("Invalid vote.\n");
                return 3;
            }
        }

        record_preferences(ranks);

        printf("\n");
    }

    add_pairs();
    sort_pairs();
    lock_pairs();
    print_winner();
    return 0;
}

// Update ranks given a new vote
bool vote(int rank, string name, int ranks[])
{
    if (name == candidates[0])
    {
        ranks[rank] = 0;
        return true;
    }
    else if (name == candidates[1])
    {
        ranks[rank] = 1;
        return true;
    }
    else if (name == candidates[2])
    {
        ranks[rank] = 2;
        return true;
    }
    else if (name == candidates[3])
    {
        ranks[rank] = 3;
        return true;
    }
    else
    {
        return false;
    }
    return false;
}

// Update preferences given one voter's ranks
void record_preferences(int ranks[])
{
    preferences[ranks[0]][ranks[1]] += 1;
    preferences[ranks[0]][ranks[2]] += 1;
    preferences[ranks[0]][ranks[3]] += 1;
    preferences[ranks[1]][ranks[2]] += 1;
    preferences[ranks[1]][ranks[3]] += 1;
    preferences[ranks[2]][ranks[3]] += 1;
    return;
}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    pair_count = 0;
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 1; j < candidate_count; j++)
        {
            if (preferences[i][j] > preferences[j][i])
            {
                pairs[pair_count].winner = i;
                pairs[pair_count].loser = j;
                pair_count++;
            }
        }
    }
    return;
}

// Sort pairs in decreasing order by strength of victory
void sort_pairs(void)
{
    for (int i = 0; i < pair_count; i++)
    {
        int max = preferences[pairs[i].winner][pairs[i].loser];
        int max_index = i;
        for (int j = i + 1; j < pair_count; j++)
        {
            if (preferences[pairs[j].winner][pairs[j].loser] > max)
            {
                max = preferences[pairs[j].winner][pairs[j].loser];
                max_index = j;
            }
        }
        pair temp = pairs[i];
        pairs[i] = pairs[max_index];
        pairs[max_index] = temp;
    }
    return;
}

// Lock pairs into the candidate graph in order, without creating cycles
void lock_pairs(void)
{
    for (int x = 0; x < pair_count; x++)
    {
        if (!circle(pairs[x].winner, pairs[x].loser)) // if no cycle created then lock pair x
        {
            locked[pairs[x].winner][pairs[x].loser] = true;
        }
    }

    return;
}

// Print the winner of the election
void print_winner(void)
{
    for (int i = 0; i < candidate_count; i++)
    {
        bool winner = true;
        for (int j = 0; j < candidate_count; j++)
        {
            if (locked[j][i] == true)
            {
                winner = false;
            }
        }
        if (winner == true)
        {
            printf("%s\n", candidates[i]);
        }
    }
    return;
}



bool circle(int a, int b)
{
    if (locked[b][a] == true)
    {
        return true;
    }
    for (int x = 0; x < pair_count; x++)
    {
        if (locked[x][a] == true)
        {
            return circle(x, b);
        }
    }
    return false;
}