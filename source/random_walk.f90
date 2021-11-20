! -*- coding: utf-8 -*-

!! Random walk 2D simulation with discrete time and space.
module random_walk

    implicit none

    private

    !! The state on 2-dimensional regular lattice.
    type, public :: state
        real :: t = 0.0; ! time
        real :: x = 0.0; ! space (x)
        real :: y = 0.0; ! space (y)
    end type

    public :: update, metrics, simulate

    contains

    pure function update(random, current) result(updated)
        !! Update the current state.
        !!
        !!    N     [0.0 ; 0.25) => LEFT  (x - 1, y) = WEST
        !!  W O E   [0.25 ; 0.5) => RIGHT (x + 1, y) = EAST
        !!    S     [0.5 ; 0.75) => DOWN  (x, y - 1) = SOUTH
        !!          [0.75 ; 1.0) => UP    (x, y + 1) = NORTH
        !!
        !! @param random  The random number.
        !! @param current The current state.
        !! @return output The updated state.
        !!
        implicit none

        ! Work-in-progress: Update-without-return, we have to provide previous move.
        ! select case (forbidden)
        ! case ('N')    print *, "North"
        ! case ('E')    print *, "East"
        ! case ('S')    print *, "South"
        ! case ('W')    print *, "West"
        ! case default  print *, "None"
        ! end select

        real,        intent(in) :: random
        type(state), intent(in) :: current
        type(state)             :: updated

        if (random < 0.0 .or. random > 1.0) then
            ! RAISE ERROR OR RETURN 0?
        end if

        updated % t = current % t + 1

        if (random >= 0.0 .and. random < 0.25) then
            updated % x = (current % x) - 1
        end if

        if (random >= 0.25 .and. random < 0.5) then
            updated % x = (current % x) + 1
        end if

        if (random >= 0.5 .and. random < 0.75) then
            updated % y = (current % y) - 1
        end if

        if (random >= 0.75 .and. random < 1.0) then
            updated % y = (current % y) + 1
        end if

    end function

    pure function simulate(trials, steps, randoms) result(outputs)
        !! Realize 2-dimensional simple random walk on ℤ for the given number of steps and trials.
        !!
        !! @param steps   The number of random walk steps.
        !! @param trials  The number of random walk trials.
        !! @param randoms The array with random numbers of size = (trials, steps)
        !! @return        The coordinates x and y.
        !!
        implicit none

        integer, intent(in) :: steps, trials
        real, intent(in) :: randoms(trials, steps)
        real, dimension(:,:,:), allocatable :: outputs
        type(state) :: current
        integer :: trial, step

        allocate(outputs(1:trials, 1:steps, 1:3))

        ! $OMP PARALLEL DO PRIVATE(current)
        do trial = 1, trials

            current % t = 0.0
            current % x = 0.0
            current % y = 0.0

            do step = 1, steps
                current = update(random=randoms(trial, step), current=current)
                outputs(trial, step, 1) = current % t
                outputs(trial, step, 2) = current % x
                outputs(trial, step, 3) = current % y
                ! print *, current
            end do

        end do
        ! $OMP END PARALLEL DO
    end function

    pure function metrics(positions) result(outputs)
        !! Compute the Euclidean distance and standard deviation.
        !! @param positons The array of `x`, `y` coordinates.
        !! @return The array with Euclidean distance and standard deviation.
        implicit none

        real, intent(in) :: positions(:,:)
        real, dimension(:,:), allocatable :: outputs
        real :: distance_average
        integer :: i

        allocate(outputs(1:size(positions, 1), 1:2)) ! 1=distance, 1=std_deviation

        do i = 1, size(positions)
            outputs(i, 1) = sqrt( positions(i, 1) ** 2 + positions(i, 2) ** 2)
        end do

        distance_average = sum(positions(:, 1)) / size(positions, 1)

        outputs(:, 2) = sqrt(  sum(((positions(:, 1) - distance_average)) ** 2) / size(positions, 1))

    end function

end module
